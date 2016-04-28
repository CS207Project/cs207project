# from .persistantdb import FILES_DIR
from collections import defaultdict
import pickle
import os

REFRESH_RATE = 50 # rate at which write_ahead log is flushed to disk

class BaseIndex:
    def __init__(self, fieldName='default', database_name='default'):
        self.database_name = database_name
        self.name = fieldName
        self.filename = 'files'+'/'+database_name+'/'+fieldName+'.idx'
        # DNY: temporary, in memory solution to be removed
        self.dict = defaultdict(set)

    def insert(self, fieldValue, pk):
        # insert the value into the appropriate place in the tree
        # DNY: need to double check that the pk is removed from other places
        # if necessary
        idx = self.dict[fieldValue]
        idx = self.dict[fieldValue]

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
