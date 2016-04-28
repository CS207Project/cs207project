from .persistantdb import FILES_DIR
import os
import pickle
import bintrees
import numpy as np

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

class BitmapIndex(BaseIndex):

    def __init__(self, values, fieldName='default', database_name='default'):

        # Init with BaseIndex
        super().__init__(fieldName, database_name)

        # 'values' is a list of possible fieldValues
        self.values = values
        self.values_len = len(values)

        # File containing the bitmap indices for this field
        self.filename = FILES_DIR+'/'+database_name+'/'+fieldName+'_index.txt'

        # File containing the pk's that are in the bitmap index
        self.pks_file = FILES_DIR+'/'+database_name+'/'+fieldName+'_pks.txt'

        # Empty list to store the the boolean arrays for the values of this field.
        #CJ: I am storing the indices as a list of numpy boolean arrays because it
        # is more memory-efficient to append to append to this list than it is to keep
        # vertically stacking numpy arrays.  
        self.bmindex_list = []
   
        # Create desired files if they don’t exist.
        # Load files if they do exist.

        # Open the associated files for updating 
        if not os.path.exists(self.filename):
            self.bmindex = open(self.filename, "xb+", buffering=0)

            self.pks = open(self.pks_file, "xb+", buffering=0)
            # Empty dictionary to store primary keys and their indices in self.bmindex
            self.pks_dict = {}
            self.dict_pks = {}
            # Empty dictionary to store self.bmindex indices and primary keys
            self.pks_len = 0
        else:
            self.bmindex = open(self.filename, "r+b", buffering=0)
            while True:
                line = self.bmindex.read(self.values_len)
                if len(line) == 0:
                    # Reached last line.
                    break
                # Use string-to-bool helper function defined below to convert the line
                #   of the text file to a boolean array, and append to the list of arrays.
                self.bmindex_list.append(str_to_bool(line))

            self.pks = open(self.pks_file, "r+b", buffering=0)
            # Read the pks file into a dictionary of 'primary key':'index in self.bmindex'
            items = [line.strip().split(b':') for line in self.pks.readlines()]
            self.pks_dict = {k:v for k,v in items}

            # Make a second dictionary keying the pks by dbindex.  This seems redundant, but
            # it makes self.getEqual() O(N) instead of O(n^2).
            self.dict_pks = {v:k for k,v in items}

            # Verify that the number of pks in the dictionary and the bmindex match
            assert len(self.bmindex_list) == len(self.pks_dict.keys()), \
                "Primary Key BMindex and position dictionary length mismatch"
            self.pks_len = len(self.pks_dict.keys())

        pass

    def insert(self, fieldValue, pk):
        # Updates the boolean array that indicates the field's values for the appropriate pk.
        # Adds pk's that are not already present, and updates pk's that are already present.  

        # Operate on string representations of pk's.
        pk_str = bytes(str(pk),'utf-8')

        # Check if the fieldValue is valid.  If not, throw an error.
        if fieldValue not in self.values:
            raise ValueError('\"{}\" not in the set of user-specified values: {}'.format(fieldValue, self.values))
        else: 
            # Check if the pk is already in the file or not.
            if pk_str not in self.pks_dict.keys():
                
                # Add the pk to the dictionary along with its index
                self.pks_dict.update({pk_str:self.pks_len})
                self.dict_pks.update({self.pks_len:pk_str})

                # Add a new line to the end of the pks file with the index
                self.pks.seek(0,2)
                self.pks.write(pk_str+b':'+bytes(str(self.pks_len),'utf-8')+b'\n')

                # Create another boolean array to append to the list of arrays
                array_to_add = np.zeros(self.values_len, dtype='bool')
                # Set the appropriate position in the array to True to indicate the field value.
                array_to_add[self.values.index(fieldValue)] = True
                # Append the array to the list of arrays
                self.bmindex_list.append(array_to_add)

                # Add a new entry to the bmindex file with the boolean array
                self.bmindex.seek(0,2)
                self.bmindex.write(bool_to_str(array_to_add))

                self.pks_len += 1

            else:
                # If the pk is already in the file, we change the value in place.

                # First, Find the index for that pk.
                pk_index = int(self.pks_dict[pk_str])

                # Next, create the array as above.
                array_to_add = np.zeros(self.values_len, dtype='bool')
                array_to_add[self.values.index(fieldValue)] = True

                # Set the list entry equal to the new array. 
                self.bmindex_list[pk_index] = array_to_add

                # Update the bmindex file
                self.bmindex.seek(pk_index*self.values_len,0)
                self.bmindex.write(bool_to_str(array_to_add))

        pass

    def getEqual(self, fieldValue):
        # Returns the list of primary keys that match this fieldValue

        # Find the index of this fieldValue in the list of valid values
        fieldValue_index = self.values.index(fieldValue)

        matching_keys = []

        # Go over list of arrays and append the indices of those that have this fieldValue.
        for ii,arr in enumerate(self.bmindex_list):
            if arr[fieldValue_index]==1:
                matching_keys.append(self.dict_pks[bytes(str(ii),'utf-8')])

        return matching_keys

    def __del__(self):
        self.bmindex.close()
        self.pks.close()

# Helper function to convert boolean arrays to byte string of 0/1 values
def bool_to_str(bool_array):
    string = ''
    for ii in bool_array:
        string+=str(int(ii))
    return bytes(string,'utf-8')

# Helper function to convert boolean strings to boolean arrays
def str_to_bool(string_line):
	decoded_string_line = string_line.decode('utf-8')
	line_len = len(decoded_string_line)
	bool_array = np.zeros(line_len, dtype='bool')
	for ii in range(line_len):
		bool_array[ii] = int(decoded_string_line[ii])
	return bool_array

