class BaseIndex:
	def __init__(self, name=‘default’, data_dir='files/default'):
        # DNY: usage to create file name-->
        # filename = data_dir+"/"+name+".idx"

		# create desired file if it doesn’t exist
		# load file if it does exist
        self.name = name
        self.type = type
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
