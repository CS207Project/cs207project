from .persistantdb import FILES_DIR
import os
import pickle
import bintrees

class BaseIndex:
	def __init__(self, fieldName='default', database_name='default'):
		# DNY: usage to create file name-->
		# create desired file if it doesn’t exist
		# load file if it does exist
		self.database_name = database_name
		self.name = fieldName
		self.filename = FILES_DIR+'/'+database_name+'/'+fieldName+'.idx'

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
		pass

	def remove(self, fieldValue, pk):
		# remove a primary key from the index
		pass

	def getEqual(self, fieldValue):
		# return set of primary keys that match this fieldValue
		pass


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
