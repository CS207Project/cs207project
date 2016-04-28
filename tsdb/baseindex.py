# from .persistantdb import FILES_DIR
from collections import defaultdict
import pickle
import os
import bintrees

REFRESH_RATE = 50 # rate at which write_ahead log is flushed to disk

class BaseIndex:
    def __init__(self, fieldName='default', database_name='default'):
        self.database_name = database_name
        self.name = fieldName
        self.filename = 'files'+'/'+database_name+'/'+fieldName+'.idx'
        # DNY: temporary, in memory solution to be removed
        self.dict = defaultdict(set)

        # load from file if the file exists
        self._loadFromFile()

        # variable that checks the staus of the in memory
        self._stale = False

    def _loadFromFile(self):
        # load the index file from disk
        pass

    def _saveToFile(self):
        # write the index back out to disk
        pass

    def deleteIndex(self):
        # delete the index file
        pass

    def insert(self, fieldValue, pk):
        # insert the value into the appropriate place in the tree
        self.dict[fieldValue].add(pk)

    def remove(self, fieldValue, pk):
        # remove a primary key from the index
        pass

    def getEqual(self, fieldValue):
        # return set of primary keys that match this fieldValue
        return self.dict[fieldValue]

class PKIndex:
    "PK Index using Pickle serialization and a write ahead log"
    def __init__(self, database_name='default'):
        # TODO DNY: write separate class for write ahead log?
        self.filename = 'files/'+database_name+'/'+'pks.p'
        self.writelog = 'files/'+database_name+'/'+'writelog.idx'

        # if file never created before, create it
        if not os.path.exists(self.filename):
            self.dict = dict()
            self.save_pickle(new=True)
        else:
            self.dict = self.load_pickle()

        if not os.path.exists(self.writelog):
            self.fd = open(self.writelog, 'x')
        else: # if log had values, load, save, and wipe them
            self.fd = self.load_and_clear_log()

        self.pk_count = len(self.dict.keys())

        self.fd.seek(0,2)#DNY: seek the end of the file
        self.writeptr = self.fd.tell()

    def load_and_clear_log(self, loaded=False):
        """
        if loaded, writelog assumed to be open. otherwise, closed.
        loads values, clears writelog and opens
        """
        if not loaded:
            self.fd = open(self.writelog,'r')
        items = [l.strip().split(':') for l in self.fd.readlines()]
        writelog_dict = {k:int(v) for k,v in items}
        self.dict.update(writelog_dict)
        self.save_pickle()
        self.fd.close()
        open(self.writelog, 'w').close() # this deletes the log
        return open(self.writelog, 'w')

    def save_pickle(self, new=False):
        form = 'xb' if new else 'wb'
        with open(self.filename, form, buffering=0) as fd:
            pickle.dump(self.dict, fd)

    def load_pickle(self):
        with open(self.filename, 'rb', buffering=0) as fd:
            return pickle.load(fd)

    def __getitem__(self, key):
        return self.dict[key]

    def __setitem__(self, key, value):
        if key not in self.dict.keys():
            self.pk_count += 1
            self.dict[key] = value
            self.fd.write(key+':'+str(value)+'\n')
            if self.pk_count % REFRESH_RATE == 0:
                self.load_and_clear_log(loaded=True)
        else:
            self.dict[key] = value

    def __iter__(self):
        return iter(self.dict.keys())

    def __contains__(self, key):
        return key in self.dict.keys()

class TreeIndex(BaseIndex):

	def _loadFromFile(self):
		if os.path.isfile(self.filename):
			with open(self.filename,'rb') as f:
				self.tree = pickle.load(f)
		else:
			print("Loading Empty Tree")
			self.tree = bintrees.AVLTree()

	def _saveToFile(self):
		with open(self.filename,'wb') as f:
			pickle.dump(self.tree, f)

	def deleteIndex(self):
		if os.path.isfile(self.filename):
			os.remove(self.filename)

	def _checkStale(self):
		if self._stale:
			self._loadFromFile()
			self._stale = False

	def insert(self,fieldValue, pk):
		self._checkStale()

		if fieldValue in self.tree:
			if pk in self.tree[fieldValue]:
				raise ValueError("primary_key already in index")
			self.tree[fieldValue] = self.tree[fieldValue] + [pk]
		else:
			self.tree[fieldValue] = [pk]
		self._saveToFile()
		self._stale = True

	def remove(self, fieldValue, pk):
		self._checkStale()

		if fieldValue in self.tree:
			matchingPks = self.tree[fieldValue]
			if pk in matchingPks:
				del matchingPks[matchingPks.index(pk)]
				self.tree[fieldValue] = matchingPks
			else:
				raise ValueError("TreeIndex.remove():: primary_key is not in the index")
		else:
			raise ValueError("TreeIndex.remove():: fieldValue is not in the index")
		self._saveToFile()
		self._stale = True

	def getEqual(self, fieldValue):
		self._checkStale()

		if fieldValue in self.tree:
			return self.tree[fieldValue]
		else:
			return []

	def getLowerThan(self, fieldValue):
		self._checkStale()
		retList = []
		for v in  self.tree[:fieldValue]:
			retList = retList + self.getEqual(v)

		return retList

	def getHigherThan(self, fieldValue):
		self._checkStale()
		retList = []
		for v in  self.tree[fieldValue:]:
			retList = retList + self.getEqual(v)

		return retList

# class BitmapIndex(BaseIndex):
#
# def getEqual(self, fieldValue):
# 		return set of primary keys that match this fieldValue
