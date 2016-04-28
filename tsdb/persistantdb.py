from collections import defaultdict
from operator import and_
from functools import reduce
import operator
import os
import numbers
# import struct
import json
import timeseries as ts
from .baseindex import BaseIndex, PKIndex
from .heap import MetaHeapFile, TSHeapFile

#// need to install these!
# import bintrees as bt #https://pypi.python.org/pypi/bintrees/2.0.2
# >>>>>>> c9bfe460ee5dee9813b69f35234642ec3947a8d4

# this dictionary will help you in writing a generic select operation
OPMAP = {
    '<': operator.lt,
    '>': operator.le,
    '==': operator.eq,
    '!=': operator.ne,
    '<=': operator.le,
    '>=': operator.ge
}

INDEXES = {
    1: None,#Binary Tree type here,
    2: None#bitmask type here
}

FILES_DIR = 'files'
MAX_CARD = 8

class PersistantDB:
    "Database implementation using Binary Trees and BitMasks"
    def __init__(self, schema, pk_field='pk', db_name='default', ts_length=1024):
        "initializes database with indexed and schema"
        # TODO DNY: if db_name already created, check to ensure that the schema
        # is the same as before
        # TODO DNY: Akhil + Christian are setting up the indexes on file
        # TODO DNY: add header file to store schema, compression string, index
        # list, etc. so that it can be loaded
        # TODO DNY: create function that eliminates deleted values in the heaps
        # TODO DNY: support non-string primary keys
        # TODO DNY: 'select' function
        # TODO DNY: change ts serialization to be fixed size

        # DNY: ensure file hierarchy is set up
        # all files to be found in './files/db_name/' directory
        self.dbname = db_name
        self.data_dir = FILES_DIR+"/"+self.dbname
        if not os.path.exists(FILES_DIR):
            os.makedirs(FILES_DIR)
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        # open heap files
        self.metaheap = MetaHeapFile(FILES_DIR+"/"+self.dbname+"/"+'metaheap')
        self.tsheap = TSHeapFile(FILES_DIR+"/"+self.dbname+"/"+'tsheap')

        self.schema = dict(schema)

        # add marker for later garbage collection upon heap compaction
        schema['deleted'] = {'type': 'bool', 'index': None}
        # marker for reading off timeseries heap file
        schema['ts_offset'] = {'type': 'int', 'index': None}

        self.pkfield = pk_field
        self.tsLength = ts_length

        # create compression schema
        self.metaheap.create_compression_string(schema)

        self.pks = PKIndex(self.dbname)

        # DNY: to store fields that will have associated indexes
        self.indexFields = [field for field, value in self.schema.items()
                                  if value['index'] is not None]
        self.indexes = {}
        for field in self.indexFields:
            self.indexes[field] = BaseIndex(field, self.dbname)
            # TODO DNY: add in functionality when new indexes are complete
            # if (schema[field]['index']==2) and (len(schema[field]['values']) <= MAX_CARD):
            #     # self.indexes[field] = BitMaskIndex()
            #     pass
            # else:
            #     # self.indexes[field] = TreeIndex()
            #     pass

    def insert_ts(self, pk, ts):
        "given a pk and a timeseries, insert them"
        # print("in db insert",pk,ts)
        # TODO DNY: rewrite once primary key index completed
        if pk in self.pks:
            raise ValueError('Duplicate primary key found during insert')

        ts_offset = self.tsheap.encode_and_write_ts(ts) # write ts to tsheap file

        # DNY: write default meta values to disk
        meta = list(self.metaheap.fieldsDefaultValues)
        meta[self.metaheap.fields.index('ts_offset')] = ts_offset
        meta[self.metaheap.fields.index('ts_offset_set')] = True
        pk_offset = self.metaheap.encode_and_write_meta(meta)

        self.pks[pk] = pk_offset
        # self.update_indices(pk)

    def _return_meta(self,pk):
        pk_offset = self.pks[pk]# DNY: temporary
        return self.metaheap.read_and_return_meta(pk_offset)

    def _return_ts(self,pk):
        # DNY: temporary testing function
        ts_offset = self._return_meta(pk)[self.metaheap.fields.index('ts_offset')]
        return self.tsheap.read_and_decode_ts(ts_offset)

    def upsert_meta(self, pk, new_meta):
        "implement upserting field values, as long as the fields are in the schema."
        # TODO DNY: Does not support updating primary keys
        # TODO DNY: Does not support deleting metadata once inserted
        pk_offset = self.pks[pk]
        meta = self.metaheap.read_and_return_meta(pk_offset)
        for n, field in enumerate(self.metaheap.fields):
            # will skip all the *_set entries
            if field in new_meta.keys():
                #TODO DNY: implement type/ error checking of the inserted values
                meta[n] = new_meta[field]
                if self.schema[field]['type'] != "bool":
                    meta[n+1] = True

        self.metaheap.encode_and_write_meta(meta, pk_offset)

        # self.update_indices(pk)

    def index_bulk(self, pks=[]):
        if len(pks) == 0:
            pks = self.pks
        for pkid in pks:
            self.update_indices(pkid)

    def update_indices(self, pk):
        "updates indices of pk with the most recent metadata"
        meta = self._return_meta(pk)
        for field in self.indexFields:
            if self.schema[field]['type'] != "bool":
                # check if not set
                field_idx = self.metaheap.fields.index(field)
                if not meta[field_idx+1]:
                    continue
            self.indexes[field].insert(pk)


    def select(self, meta, fields_to_ret, additional):
        pass
        #
        # pks_out = set(self.rows.keys())
        # for field,criteria in meta.items():
        #     if field in self.schema:
        #         fieldConvert = self.schema[field]['convert']
        #
        #         #ASK: this is a range query. Not sure how to do this with indices with
        #         #     current implementation
        #         if(isinstance(criteria,dict)):
        #             op,val = list(criteria.items())[0]
        #             matches = [p for p in pks_out if field in self.rows[p] and
        #                             OPMAP[op](self.rows[p][field],fieldConvert(val))]
        #             pks_out = pks_out & set(matches)
        #
        #         #ASK: this is an exact query
        #         else:
        #             criteria = fieldConvert(criteria) #ASK: convert to the right format
        #
        #             #ASK: we have an index for this field
        #             if field in self.indexes:
        #                 matches = self.indexes[field][criteria]
        #
        #             #ASK: we don't have an index for this field
        #             else:
        #                 matches = [p for p in pks_out if field in self.rows[p] and
        #                             self.rows[p][field] == criteria]
        #             pks_out = pks_out & set(matches)
        #
        # #ASK: decide what to return
        # pks_out = list(pks_out)
        # if additional and 'sort_by' in additional:
        #     # print("Sorting by ",additional['sort_by'][1:]," in direction ",additional['sort_by'][0])
        #     sortfield = additional['sort_by'][1:]
        #     sortdir = additional['sort_by'][0]
        #
        #     if sortfield not in self.schema:
        #         raise Exception("Sort Column not in schema")
        #
        #     if sortdir == '+':
        #         pks_out = sorted(pks_out,key=lambda p: self.rows[p][sortfield])
        #     elif sortdir == '-':
        #         pks_out = sorted(pks_out,key=lambda p: self.rows[p][sortfield],reverse=True)
        #     else:
        #         raise Exception("Illdefined sort order. Must be '+' or '-'")
        #
        # if additional and 'limit' in additional:
        #     print("Limiting")
        #     pks_out = pks_out[:int(additional['limit'])]
        #
        # return self._getDataForRows(pks_out,fields_to_ret)
