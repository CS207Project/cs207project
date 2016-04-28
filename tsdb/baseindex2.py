from persistantdb import FILES_DIR
from collections import defaultdict

class BaseIndex:
	def __init__(self, fieldName='default', database_name='default'):
        self.database_name = database_name
        self.name = fieldName
        self.filename = FILES_DIR+'/'+database_name+'/'+fieldName+'.idx'
        # DNY: temporary, in memory solution to be removed
        self.dict = defaultdict(set)

	def insert(self, fieldValue, pk):
		# insert the value into the appropriate place in the tree
		idx = self.dict[fieldValue]
        idx.add(pk)

	def getEqual(self, fieldValue):
		# return set of primary keys that match this fieldValue
		return self.dict[fieldValue]
