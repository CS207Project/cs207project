from persistantdb import FILES_DIR

class BaseIndex:
	def __init__(self, fieldName=‘default’, database_name='default'):
        # DNY: usage to create file name-->
		# create desired file if it doesn’t exist
		# load file if it does exist
        self.database_name = database_name
        self.name = fieldName
        self.filename = FILES_DIR+'/'+database_name+'/'+fieldName+'.idx'
		pass

	def insert(self, fieldValue, pk):
		# insert the value into the appropriate place in the tree
		pass

	def getEqual(self, fieldValue):
		# return set of primary keys that match this fieldValue
		pass


# class TreeIndex(BaseIndex):
#
# 	def getLowerThan(self, fieldValue):
# 		# return set of pks
#
# def getHigherThan(self, fieldValue):
# 		# return set of pks
#
# class BitmapIndex(BaseIndex):
#
# def getEqual(self, fieldValue):
		# return set of primary keys that match this fieldValue
