"""All the index classes.

Currentlly:
    PKIndex: Primary Key Index
    TreeIndex: Tree based index done using a AVL tree
    BitmapIndex: Bitmap index for low cardinality columns
"""

# from .persistentdb import FILES_DIR
from .baseclasses import BaseIndex
from collections import defaultdict
import pickle
import os
import bintrees
import numpy as np

REFRESH_RATE = 50 # rate at which write_ahead log is flushed to disk

class SimpleIndex(BaseIndex):
    """Very simple index that implements a default dict
    """
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

    def insert(self, fieldValue, pk):
        # insert the value into the appropriate place in the tree
        self.dict[fieldValue].add(pk)

    def remove(self, fieldValue, pk):
        if fieldValue in self.dict[fieldValue]:
            self.dict[fieldValue].remove(pk)

    def getEqual(self, fieldValue):
        # return set of primary keys that match this fieldValue
        return self.dict[fieldValue]

class PKIndex(BaseIndex):
    """
    PK Index using Pickle serialization and a write ahead log.
    Essentially a (pk: offset) dictionary with writelog and disk storage.
    """
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

    def load_and_clear_log(self, loaded=False, close=False):
        """
        if loaded, writelog assumed to be open. otherwise, closed.
        loads values, clears writelog and opens.
        if close, then file descriptor not return.
        """
        if loaded:
            self.fd.close()
        self.fd = open(self.writelog,'r')
        items = [l.strip().split(':') for l in self.fd.readlines()]
        writelog_dict = {k:int(v) for k,v in items}
        self.dict.update(writelog_dict)
        self.save_pickle()
        self.fd.close()
        open(self.writelog, 'w').close() # this deletes the log
        if not close:
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
                self.fd = self.load_and_clear_log(loaded=True)
        else:
            self.dict[key] = value

    def __iter__(self):
        return iter(self.dict.keys())

    def __contains__(self, key):
        return key in self.dict.keys()

    def keys(self):
        return self.dict.keys()

    def __len__(self):
        return self.pk_count

    def insert(self, key, value):
        # insert the value into the appropriate place in the tree
        # delegates to __setitem__
        self[key] = value

    def remove(self, key, value=None):
        # added to match interface. Value unnecessary here.
        self.fd = self.load_and_clear_log(loaded=True)
        del self.dict[key]
        self.save_pickle()

    def getEqual(self, key):
        return self[key]

    def close(self):
        self.load_and_clear_log(loaded=True, close=True)

class TreeIndex(SimpleIndex):

    def _loadFromFile(self):
        if os.path.isfile(self.filename):
            with open(self.filename,'rb') as f:
                self.tree = pickle.load(f)
        else:
            # print("Loading Empty Tree")
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
            if pk not in self.tree[fieldValue]:
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
            import pdb; pdb.set_trace()
            raise ValueError("TreeIndex.remove():: fieldValue is not in the index")
        self._saveToFile()
        self._stale = True

    def get(self, fieldValue, operator_num=2):
        """
        'get' wrapper function to delegate to other functions
        based on submitted operator
        """
        if operator_num == 0:
            return self.getLowerThan(fieldValue)
        elif operator_num == 1:
            return self.getHigherThan(fieldValue)
        elif operator_num == 2:
            return self.getEqual(fieldValue)
        elif operator_num == 3:
            return self.getNotEq(fieldValue)
        elif operator_num == 4:
            return self.getLowerOrEq(fieldValue)
        elif operator_num == 5:
            return self.getHigherOrEq(fieldValue)
        raise RuntimeError("should be impossible")

    def getEqual(self, fieldValue):
        self._checkStale()

        if fieldValue in self.tree:
            return set(self.tree[fieldValue])
        else:
            return set()

    def getLowerThan(self, fieldValue):
        self._checkStale()
        retList = set()
        for v in self.tree[:fieldValue]:
            retList = retList | self.getEqual(v)

        return set(retList)

    def getHigherThan(self, fieldValue):
        self._checkStale()
        retList = set()
        for v in self.tree[fieldValue:]:
            if v != fieldValue:
                retList = retList | self.getEqual(v)
        return set(retList)

    def allKeys(self):
        pks = set()
        for value in self.trees.values():
            pks = pks | value
        return pks

    def getHigherOrEq(self, fieldValue):
        return self.getHigherThan(fieldValue) | self.getEqual(fieldValue)

    def getLowerOrEq(self, fieldValue):
        return self.getLowerThan(fieldValue) | self.getEqual(fieldValue)

    def getNotEq(self, fieldValue):
        return self.allKeys() - self.getEqual(fieldValue)



class BitmapIndex:

    def __init__(self, values, pk_len = 4, fieldName='default', database_name='default'):
        # Requires the user to specify pk_len, the fixed length of the primary keys
        self.pks_len = pk_len
        
        # 'values' is a list of possible fieldValues
        self.values = values
        self.values_len = len(values)

        # File containing the bitmap indices for this field
        self.filename = 'files/'+database_name+'/'+fieldName+'_index.txt'

        # Empty list to store the the lists of booleans for each field value.  
        #CJ: I am storing the indices as a list of list of boolean because it
        # is more memory-efficient to append to append to the lists than it is to keep
        # vertically stacking numpy arrays.
        self.bmindex_list = [[] for ii in range(self.values_len)]

        # Empty dictionary to store primary keys and their indices in self.bmindex
        self.pks_dict = {}
        self.dict_pks = {}
        
        # Create desired files if they don’t exist.
        # Load files if they do exist.

        # Open the associated files for updating
        if not os.path.exists(self.filename):
            self.bmindex = open(self.filename, "xb+", buffering=0)
            self.last_pk_idx = 0

        else:
            # Load from file
            
            item_counter = 0
            
            self.bmindex = open(self.filename, "r+b", buffering=0)
            while True:
                # Try to read the primary key for this line
                prim_key = self.bmindex.read(self.pks_len)
                if prim_key == b'':
                    # Reached last line.
                    break
                elif prim_key in self.pks_dict.keys():
                    del self.dict_pks[self.pks_dict[prim_key]]
                self.pks_dict.update({prim_key:item_counter})
                self.dict_pks.update({item_counter:prim_key})
                
                for ii in range(self.values_len):
                    try:
                        boolean = bool(int(self.bmindex.read(1)))
                        self.bmindex_list[ii].append(boolean)
                    except ValueError:
                        # Thrown if the sentinel value of b'-' has been written
                        del self.pks_dict[prim_key]
                        del self.dict_pks[item_counter]
                        break
                
                item_counter += 1
            
            self.last_pk_idx = item_counter

    def insert(self, fieldValue, pk):
        # Updates the booleans that indicate the field's values for the appropriate pk.
        # Adds pk's that are not already present, and updates pk's that are already present.

        # Pk's are stored as bytes, so if the user passed ints or strings, convert to bytes.
        if type(pk) != 'bytes':
            pk_str = bytes(str(pk),'utf-8')
        else:
            pk_str = pk
            
        if len(pk_str) != self.pks_len:
            raise ValueError("Primary key {} is not of the pre-specified length {}".format(pk,self.pks_len))

        # Check if the fieldValue is valid.  If not, throw an error.
        if fieldValue not in self.values:
            raise ValueError('\"{}\" not in the set of user-specified values: {}'.format(fieldValue, self.values))
        else:
            # Find field index from the objects values
            field_index = self.values.index(fieldValue)
            
            # Add the pk to the dictionary along with its index
            if pk_str in self.pks_dict.keys():
                del self.dict_pks[self.pks_dict[pk_str]]
                del self.pks_dict[pk_str]
                
            self.pks_dict.update({pk_str:self.last_pk_idx})
            self.dict_pks.update({self.last_pk_idx:pk_str})
            
            self.last_pk_idx += 1

            # Add the pk and the booleans to the end of the file
            self.bmindex.seek(0,2)
            self.bmindex.write(pk_str)
            
            # Update the in-memory lists and write to file
            for ii in range(self.values_len):
                if ii==field_index:
                    self.bmindex_list[ii].append(True)
                    self.bmindex.write(b'1')
                else:
                    self.bmindex_list[ii].append(False)
                    self.bmindex.write(b'0')

    def remove(self, pk):
        # Removes the entry for this field and primary key from the database
        
        if type(pk) != 'bytes':
            pk_str = bytes(str(pk),'utf-8')

        # Check if the pk is in the file or not.
        if pk_str not in self.pks_dict.keys():
            raise KeyError('\"{}\" not a valid primary key'.format(pk))
        else:
            # Remove the primary key from the dictionaries
            del self.dict_pks[self.pks_dict[pk_str]]
            del self.pks_dict[pk_str]
            
            # Write a sentinel value to the persistent database
            self.bmindex.write(pk_str + (self.values_len*b'-'))


    def getEqual(self, fieldValue):
        # Returns the list of primary keys that match this fieldValue

        # Find the index of this fieldValue in the list of valid values
        if fieldValue not in self.values:
            raise ValueError('\"{}\" not in the set of user-specified values: {}'.format(fieldValue, self.values))
        else:
            fieldValue_index = self.values.index(fieldValue)

            matching_keys = []

            for ii in self.dict_pks.keys():
                if self.bmindex_list[fieldValue_index][ii] == True:
                    matching_keys.append(self.dict_pks[ii])

            return set(matching_keys)
    
    def getNotEq(self, fieldValue):
        if fieldValue not in self.values:
            raise ValueError('\"{}\" not in the set of user-specified values: {}'.format(fieldValue, self.values))
        else:
            fieldValue_index = self.values.index(fieldValue)
            
            matching_keys = []
            
            for ii in self.dict_pks.keys():
                if self.bmindex_list[fieldValue_index][ii] == False:
                    matching_keys.append(self.dict_pks[ii])
            
            return set(matching_keys)
        
    def allKeys(self):
        return set(self.pks_dict.keys())
    
    def deleteIndex(self):
        if os.path.isfile(self.filename):
            os.remove(self.filename)
            
    def get(self,pk):
        index = self.pks_dict[bytes(pk, 'utf-8')]
        for ii in range(self.values_len):
            value_index = self.bmindex_list[ii][index]
            if value_index == True:
                return self.values[ii]
            
    def __del__(self):
        self.bmindex.close()



# class BitmapIndex(BaseIndex):

#     def __init__(self, values, fieldName='default', database_name='default'):

#         # Init with BaseIndex
#         super().__init__(fieldName, database_name)

#         # 'values' is a list of possible fieldValues
#         self.values = values
#         self.values_len = len(values)

#         # File containing the bitmap indices for this field
#         self.filename = 'files/'+database_name+'/'+fieldName+'_index.txt'

#         # File containing the pk's that are in the bitmap index
#         self.pks_file = 'files/'+database_name+'/'+fieldName+'_pks.txt'

#         # Empty list to store the the boolean arrays for the values of this field.
#         #CJ: I am storing the indices as a list of numpy boolean arrays because it
#         # is more memory-efficient to append to append to this list than it is to keep
#         # vertically stacking numpy arrays.
#         self.bmindex_list = []

#         # Create desired files if they don’t exist.
#         # Load files if they do exist.

#         # Open the associated files for updating
#         if not os.path.exists(self.filename):
#             self.bmindex = open(self.filename, "xb+", buffering=0)

#             self.pks = open(self.pks_file, "xb+", buffering=0)
#             # Empty dictionary to store primary keys and their indices in self.bmindex
#             self.pks_dict = {}
#             self.dict_pks = {}
#             # Empty dictionary to store self.bmindex indices and primary keys
#             self.pks_len = 0
#         else:
#             self.bmindex = open(self.filename, "r+b", buffering=0)
#             while True:
#                 line = self.bmindex.read(self.values_len)
#                 if len(line) == 0:
#                     # Reached last line.
#                     break
#                 # Use string-to-bool helper function defined below to convert the line
#                 #   of the text file to a boolean array, and append to the list of arrays.
#                 self.bmindex_list.append(str_to_bool(line))

#             self.pks = open(self.pks_file, "r+b", buffering=0)
#             # Read the pks file into a dictionary of 'primary key':'index in self.bmindex'
#             items = [line.strip().split(b':') for line in self.pks.readlines()]
#             self.pks_dict = {k:v for k,v in items}

#             # Make a second dictionary keying the pks by dbindex.  This seems redundant, but
#             # it makes self.getEqual() O(N) instead of O(n^2).
#             self.dict_pks = {v:k for k,v in items}

#             # Verify that the number of pks in the dictionary and the bmindex match
#             assert len(self.bmindex_list) == len(self.pks_dict.keys()), \
#                 "Primary Key BMindex and position dictionary length mismatch"
#             self.pks_len = len(self.pks_dict.keys())

#         pass

#     def insert(self, fieldValue, pk):
#         # Updates the boolean array that indicates the field's values for the appropriate pk.
#         # Adds pk's that are not already present, and updates pk's that are already present.

#         # Operate on string representations of pk's.
#         pk_str = bytes(str(pk),'utf-8')

#         # Check if the fieldValue is valid.  If not, throw an error.
#         if fieldValue not in self.values:
#             raise ValueError('\"{}\" not in the set of user-specified values: {}'.format(fieldValue, self.values))
#         else:
#             # Check if the pk is already in the file or not.
#             if pk_str not in self.pks_dict.keys():

#                 # Add the pk to the dictionary along with its index
#                 self.pks_dict.update({pk_str:self.pks_len})
#                 self.dict_pks.update({self.pks_len:pk_str})

#                 # Add a new line to the end of the pks file with the index
#                 self.pks.seek(0,2)
#                 self.pks.write(pk_str+b':'+bytes(str(self.pks_len),'utf-8')+b'\n')

#                 # Create another boolean array to append to the list of arrays
#                 array_to_add = np.zeros(self.values_len, dtype='bool')
#                 # Set the appropriate position in the array to True to indicate the field value.
#                 array_to_add[self.values.index(fieldValue)] = True
#                 # Append the array to the list of arrays
#                 self.bmindex_list.append(array_to_add)

#                 # Add a new entry to the bmindex file with the boolean array
#                 self.bmindex.seek(0,2)
#                 self.bmindex.write(bool_to_str(array_to_add))

#                 self.pks_len += 1

#             else:
#                 # If the pk is already in the file, we change the value in place.

#                 # First, Find the index for that pk.
#                 pk_index = int(self.pks_dict[pk_str])

#                 # Next, create the array as above.
#                 array_to_add = np.zeros(self.values_len, dtype='bool')
#                 array_to_add[self.values.index(fieldValue)] = True

#                 # Set the list entry equal to the new array.
#                 self.bmindex_list[pk_index] = array_to_add

#                 # Update the bmindex file
#                 self.bmindex.seek(pk_index*self.values_len,0)
#                 self.bmindex.write(bool_to_str(array_to_add))

#         pass

#     def remove(self, fieldValue, pk):
#         # Removes the entry for this field and primary key from the database
#         # Operate on string representations of pk's.
#         pk_str = bytes(str(pk),'utf-8')

#         # Check if the fieldValue is valid.  If not, throw an error.
#         if fieldValue not in self.values:
#             raise ValueError('\"{}\" not in the set of user-specified values: {}'.format(fieldValue, self.values))
#         else:
#             # Check if the pk is in the file or not.
#             if pk_str not in self.pks_dict.keys():
#                 raise KeyError('\"{}\" not a valid primary key'.format(pk))
#             else:
#                 # remove the index in bmindex_list from the dictionary of primary keys
#                 index = int(self.pks_dict.pop(pk_str))
#                 # remove the pk from the dictionary that keys pk by index
#                 del self.dict_pks[index]
#                 # delete pk from self.pks
#                 del self.pks[pk_str]
#                 # delete the boolean array from the list of arrays
#                 del self.bmindex_list[index]
#                 # delete index from persistent bmindex file
                
#                 # delete from persistent pks_file
                

#                 self.pks_len -= 1


#     def getEqual(self, fieldValue):
#         # Returns the list of primary keys that match this fieldValue

#         # Find the index of this fieldValue in the list of valid values
#         fieldValue_index = self.values.index(fieldValue)

#         matching_keys = []

#         # Go over list of arrays and append the indices of those that have this fieldValue.
#         for ii,arr in enumerate(self.bmindex_list):
#             if arr[fieldValue_index]==1:
#                 matching_keys.append(self.dict_pks[bytes(str(ii),'utf-8')])

#         return matching_keys

#     def __del__(self):
#         self.bmindex.close()
#         self.pks.close()

# # Helper function to convert boolean arrays to byte string of 0/1 values
# def bool_to_str(bool_array):
#     string = ''
#     for ii in bool_array:
#         string+=str(int(ii))
#     return bytes(string,'utf-8')

# # Helper function to convert boolean strings to boolean arrays
# def str_to_bool(string_line):
#     decoded_string_line = string_line.decode('utf-8')
#     line_len = len(decoded_string_line)
#     bool_array = np.zeros(line_len, dtype='bool')
#     for ii in range(line_len):
#         bool_array[ii] = int(decoded_string_line[ii])
#     return bool_array
