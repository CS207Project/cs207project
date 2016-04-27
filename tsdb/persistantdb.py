from collections import defaultdict
from operator import and_
from functools import reduce
import operator
import os
import numbers
import struct
import json
import timeseries as ts

#// need to install these!
import bintrees as bt#https://pypi.python.org/pypi/bintrees/2.0.2
import pybloomfilter as bf

# this dictionary will help you in writing a generic select operation
OPMAP = {
    '<': operator.lt,
    '>': operator.le,
    '==': operator.eq,
    '!=': operator.ne,
    '<=': operator.le,
    '>=': operator.ge
}

# see https://docs.python.org/3.4/library/struct.html#struct-format-strings
TYPES = {
    'float': 'd',
    'bool': '?',
    'int': 'i'
}

TYPE_DEFAULT = {
    'float': 0.0,
    'bool': False,
    'int': 0
}

INDEXES = {
    1: None,#Binary Tree type here,
    2: None#bitmask type here
}

FILES_DIR = 'files'

TS_FIELD_LENGTH = 4

class PersistantDB:
    "Database implementation using Binary Trees and BitMasks"
    def __init__(self, schema,pk_field = 'pk',db_name = 'default', ts_length=1024):
        "initializes database with indexed and schema"
        self.dbname = db_name# all files to be found in './files/db_name/' directory
        self.data_dir = FILES_DIR+"/"+self.dbname
        self.metaHeapFile = FILES_DIR+"/"+self.dbname+"/"+'metaheap'
        self.tsHeapFile = FILES_DIR+"/"+self.dbname+"/"+'tsheap'
        # TODO: DNY: Set up the indexes on file

        # ensure file hierarchy is set up
        if not os.path.exists(FILES_DIR):
            os.makedirs(FILES_DIR)
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        # open the associated files for reading meta data
        if not os.path.exists(self.metaHeapFile):
            #DNY: buffering=0 only allowed in binary mode, see python docs
            self.metafd = open(self.metaHeapFile, "xb+", buffering=0)
        else:
            self.metafd = open(self.metaHeapFile, "r+b", buffering=0)
            # TODO: DNY: add indexing into heap files via binary trees
        self.meta_readptr = self.metafd.tell()
        self.metafd.seek(0,2)#DNY: seek the end of the file
        self.meta_writeptr = self.metafd.tell()

        # open the associated files for reading meta data
        if not os.path.exists(self.tsHeapFile):
            #DNY: buffering=0 only allowed in binary mode, see python docs
            self.tsfd = open(self.tsHeapFile, "xb+", buffering=0)
        else:
            self.tsfd = open(self.tsHeapFile, "r+b", buffering=0)
        self.ts_readptr = self.tsfd.tell()
        self.tsfd.seek(0,2)#DNY: seek the end of the file
        self.ts_writeptr = self.tsfd.tell()

        # TODO: DNY: need to figure out how to check if passed in values are the
        # same as the information existing in memory already

        # marker for later garbage collection in the metaheap and tsheap files
        schema['deleted'] = {'type': 'bool', 'index': None}
        # marker for reading off timeseries heap file
        schema['ts_offset'] = {'type': 'int', 'index': None} #DNY: temporary, is 'int' large enough?

        self.pkfield = pk_field
        self.tsLength = ts_length
        self.compression_string = self._create_compression_string(schema)
        self.canonicalByteArrayLength = len(struct.pack(self.compression_string,*self.defaultMeta))
        self.schema = schema

        # self.pkIndex = bt.RBTree()# tree keyed on 'pk'
        # self.otherIndexes = {}
        self.pks = {} #DNY: temporary, for testing

        # TODO DNY: create indexes

    def _create_compression_string(self, schema):
        fieldList = list(schema.keys())
        fieldList.remove('ts')
        fieldList.remove('pk')# pk and ts will be stored in the index file and tsheap file respectively
        sorted(fieldList)
        self.metaFields = []# DNY: ordered list of storage of fields
        self.defaultMeta = []# DNY: to store default values of each field, as placeholders
        compression_string = ''
        for field in fieldList:
            compression_string += TYPES[schema[field]['type']]
            self.metaFields.append(field)
            self.defaultMeta.append(TYPE_DEFAULT[schema[field]['type']])
            if schema[field]['type'] != "bool":# to check whether field is set, later
                compression_string += TYPES['bool']
                self.metaFields.append(field+"_set")
                self.defaultMeta.append(False)
        return compression_string

    def insert_ts(self, pk, ts):
        "given a pk and a timeseries, insert them"
        # print("in db insert",pk,ts)
        # TODO DNY: temporary storage for pk. to move to binary tree on disk
        if pk not in self.pks:
            self.pks[pk] = {'pk': pk}
        else:
            raise ValueError('Duplicate primary key found during insert')

        ts_offset = self._encode_and_write_ts(ts) # write ts to tsheap file

        # DNY: write default
        meta = list(self.defaultMeta)
        meta[self.metaFields.index('ts_offset')] = ts_offset
        meta[self.metaFields.index('ts_offset_set')] = True
        self._encode_and_write_meta(pk, meta)
        # self.update_indices(pk)

    def _encode_and_write_ts(self, ts):
        dataBytes = json.dumps(ts.to_json()).encode()
        lengthFieldBytes = (len(dataBytes)+TS_FIELD_LENGTH).to_bytes(TS_FIELD_LENGTH, byteorder='little')
        byteArray = lengthFieldBytes + dataBytes

        self.tsfd.seek(self.ts_writeptr)
        ts_offset = self.tsfd.tell()
        self.tsfd.write(byteArray)
        self.tsfd.seek(0,2)#DNY: seek the end of the file
        self.ts_writeptr = self.tsfd.tell()
        return ts_offset

    def _read_and_decode_ts(self, offset):
        self.tsfd.seek(offset)
        ts_length = int.from_bytes(self.tsfd.read(TS_FIELD_LENGTH), byteorder='little')
        self.tsfd.seek(offset + TS_FIELD_LENGTH)
        buff = self.tsfd.read(ts_length)
        return ts.TimeSeries.from_json(json.loads(buff.decode()))

    def _encode_and_write_meta(self, pk, meta):
        byteArray = struct.pack(self.compression_string,*meta)
        self._check_byteArray(byteArray)
        if 'offset' not in self.pks[pk].keys():# if not set, find correct spot
            self.pks[pk]['offset'] = self.meta_writeptr
        self.metafd.seek(self.pks[pk]['offset'])
        self.metafd.write(byteArray)
        # self.metafd.seek(0,2)#DNY: seek the end of the file
        # self.meta_writeptr = self.metafd.tell()

    def _check_byteArray(self,byteArray):
        assert(len(byteArray) == self.canonicalByteArrayLength)

    def _read_and_return_meta(self,pk):
        offset = self.pks[pk]['offset']
        self.metafd.seek(offset)
        buff = self.metafd.read(self.canonicalByteArrayLength)
        #check that reading and writing worked
        # print(self.metaFields)
        # print(struct.unpack(self.compression_string,buff))
        return list(struct.unpack(self.compression_string,buff))

    def upsert_meta(self, pk, new_meta):
        # DNY: Does not support updating primary keys
        # DNY: Does not support deleting metadata once inserted
        "implement upserting field values, as long as the fields are in the schema."
        #TODO DNY: catch error if pk not in db already
        offset = self.pks[pk]['offset']#temporary
        meta = self._read_and_return_meta(pk)
        for n, field in enumerate(self.metaFields):
            # will skip all the *_set entries
            if field in new_meta.keys():
                #TODO DNY: implement type/ error checking of the inserted values
                meta[n] = new_meta[field]
                if self.schema[field]['type'] != "bool":
                    meta[n+1] = True

        self._encode_and_write_meta(pk, meta)

        # self.update_indices(pk)

    def index_bulk(self, pks=[]):
        pass

    def update_indices(self, pk):
        pass

    def select(self, meta, fields_to_ret, additional):
        pass
#
# class DictDB:
#     "Database implementation in a dict"
#     def __init__(self, schema,pk_field = 'pk'):
#         "initializes database with indexed and schema"
#         self.indexes = {}
#         self.rows = {} # contains the row data, each entry points to another dictionary
#         self.schema = schema # DNY: see go_server.py for example schema
#         self.pkfield = pk_field
#         for s in schema:
#             indexinfo = schema[s]['index']
#             # convert = schema[s]['convert']
#             # later use binary search trees for highcard/numeric
#             # bitmaps for lowcard/str_or_factor
#             if indexinfo is not None:
#                 self.indexes[s] = defaultdict(set)# create an index for every non-None schema
#
#     def insert_ts(self, pk, ts):
#         "given a pk and a timeseries, insert them"
#         print("in db insert",pk,ts)
#         if pk not in self.rows:
#             self.rows[pk] = {'pk': pk}
#         else:
#             raise ValueError('Duplicate primary key found during insert')
#         self.rows[pk]['ts'] = ts
#         self.update_indices(pk)
#
#     def upsert_meta(self, pk, meta):
#         "implement upserting field values, as long as the fields are in the schema."
#         #DNY written
#         # assume meta is a dict, field->values
#         for field, value in meta.items():
#             if field in self.schema:# ignore all fields not in schema
#                 if pk not in self.rows:# assert that timeseries already exists
#                     raise ValueError('Primary key not found in database')
#                 fieldConvert = self.schema[field]['convert']
#                 self.rows[pk][field] = fieldConvert(value)
#         self.update_indices(pk)
#
#     def index_bulk(self, pks=[]):
#         if len(pks) == 0:
#             pks = self.rows
#         for pkid in pks:#DNY: I think this was a mistake. formerly 'self.pks:'
#             self.update_indices(pkid)
#
#     def update_indices(self, pk):
#         row = self.rows[pk]
#         for field in row:#DNY: eg 'pk' or 'ts', or any entry in self.schema
#             v = row[field]
#             if self.schema[field]['index'] is not None:
#                 idx = self.indexes[field]# idx is a defaultdict(set)
#                 idx[v].add(pk)#DNY: 'v' must be hashable
#
#     #ASK: Helper func
#     def _getDataForRows(self,pks_out,fields_to_ret):
#         data_list_out = []
#
#         # just return primary_key and empty dicts
#         if fields_to_ret is None:
#             data_list_out = [{} for _ in range(len(pks_out))]
#
#         # return all fields except for the 'ts' field
#         elif fields_to_ret == []:
#             for p in pks_out:
#                 values_dict = self.rows[p]
#                 data_list_out.append(
#                     {field:value for field,value in values_dict.items() if field != 'ts'})
#
#         # return all fields that the user has specified
#         elif isinstance(fields_to_ret,list):
#             for p in pks_out:
#                 values_dict = self.rows[p]
#                 data_list_out.append(
#                     {field:value for field,value in values_dict.items() if field in fields_to_ret})
#
#         # something went wrong
#         else:
#             raise Exception("Fields requested must be a list or None")
#
#         return pks_out, data_list_out
#
#     def select(self, meta, fields_to_ret, additional):
#         #ASK: Implementing via a full table scan right now
#
#         pks_out = set(self.rows.keys())
#         for field,criteria in meta.items():
#             if field in self.schema:
#                 fieldConvert = self.schema[field]['convert']
#
#                 #ASK: this is a range query. Not sure how to do this with indices with
#                 #     current implementation
#                 if(isinstance(criteria,dict)):
#                     op,val = list(criteria.items())[0]
#                     matches = [p for p in pks_out if field in self.rows[p] and
#                                     OPMAP[op](self.rows[p][field],fieldConvert(val))]
#                     pks_out = pks_out & set(matches)
#
#                 #ASK: this is an exact query
#                 else:
#                     criteria = fieldConvert(criteria) #ASK: convert to the right format
#
#                     #ASK: we have an index for this field
#                     if field in self.indexes:
#                         matches = self.indexes[field][criteria]
#
#                     #ASK: we don't have an index for this field
#                     else:
#                         matches = [p for p in pks_out if field in self.rows[p] and
#                                     self.rows[p][field] == criteria]
#                     pks_out = pks_out & set(matches)
#
#         #ASK: decide what to return
#         pks_out = list(pks_out)
#         if additional and 'sort_by' in additional:
#             # print("Sorting by ",additional['sort_by'][1:]," in direction ",additional['sort_by'][0])
#             sortfield = additional['sort_by'][1:]
#             sortdir = additional['sort_by'][0]
#
#             if sortfield not in self.schema:
#                 raise Exception("Sort Column not in schema")
#
#             if sortdir == '+':
#                 pks_out = sorted(pks_out,key=lambda p: self.rows[p][sortfield])
#             elif sortdir == '-':
#                 pks_out = sorted(pks_out,key=lambda p: self.rows[p][sortfield],reverse=True)
#             else:
#                 raise Exception("Illdefined sort order. Must be '+' or '-'")
#
#         if additional and 'limit' in additional:
#             print("Limiting")
#             pks_out = pks_out[:int(additional['limit'])]
#
#         return self._getDataForRows(pks_out,fields_to_ret)
