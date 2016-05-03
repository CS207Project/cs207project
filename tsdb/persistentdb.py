"""Persistent time series database.
"""

from collections import defaultdict
from operator import and_
from functools import reduce
import operator
import os
import numbers
# import struct
import json
import timeseries
from .indices import BaseIndex, PKIndex, TreeIndex
from .heap import MetaHeapFile, TSHeapFile
from .baseclasses import BaseDB
import pickle
import shutil

#// need to install these!
# import bintrees as bt #https://pypi.python.org/pypi/bintrees/2.0.2
# >>>>>>> c9bfe460ee5dee9813b69f35234642ec3947a8d4

# this dictionary will help you in writing a generic select operation
OPMAP = {
    '<': 0,
    '>': 1,
    '==': 2,
    '!=': 3,
    '<=': 4,
    '>=': 5
}

INDEXES = {
    1: None,#Binary Tree type here,
    2: None#bitmask type here
}

FILES_DIR = 'files'
MAX_CARD = 8

def dict_eq(dict1, dict2):
    if not sorted(list(dict1.keys()))==sorted(list(dict2.keys())):
        # import pdb; pdb.set_trace()
        return False
    eq = True
    for key in dict1.keys():
        if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
            eq = (eq and dict_eq(dict1[key],dict2[key]))
        else:
            eq = (eq and (dict1[key]==dict2[key]))
        if not eq:
            # import pdb; pdb.set_trace()
            # print("not equal on ",key)
            break
    return eq


class PersistentDB(BaseDB):
    """
    Database implementation to allow for persistent storage. It's implemented
    using Binary Trees and BitMasks.
    """
    def __init__(self, schema=None, pk_field='pk', db_name='default', ts_length=1024, testing=False):
        """Initializes database with index and schema."""
        # TODO DNY: set up bitmask indexes

        # COULD DO DNY: create function that eliminates deleted values in the heaps
        # COULD DO DNY: support non-string primary keys

        # DNY: ensure file hierarchy is set up
        # all files to be found in './files/db_name/' directory
        if not testing and db_name == 'testing':
            raise ValueError("database name 'testing' reserved for database testing")

        self.dbname = db_name
        self.data_dir = FILES_DIR+"/"+self.dbname
        if not os.path.exists(FILES_DIR):
            os.makedirs(FILES_DIR)
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        # load db_metadata if it exists, or write it if new
        if os.path.exists(self.data_dir+"/db_metadata.met"):
            with open(self.data_dir+"/db_metadata.met", 'rb', buffering=0) as fd:
                self.tsLength, self.pkfield, self.schema = pickle.load(fd)
                if schema is not None:
                    try:
                        assert(dict_eq(schema, self.schema))
                    except:
                        # import pdb; pdb.set_trace()
                        raise ValueError("schema does not match stored schema. pass in schema=None")
                try:
                    assert(self.pkfield == pk_field)
                except:
                    raise ValueError("PK field does not match stored pk. PK field should be '{}'".format(self.pkfield))
                try:
                    assert(self.tsLength == ts_length)
                except:
                    raise ValueError("ts_length field does not match stored value. ts_length field should be '{}'".format(self.tsLength))
                # print("old db values loaded, assertions passed")
        else:
            self.tsLength = ts_length
            self.pkfield = pk_field
            self.schema = dict(schema)
            with open(self.data_dir+"/db_metadata.met",'xb',buffering=0) as fd:
                pickle.dump((self.tsLength, self.pkfield, self.schema), fd)
            # add metavalues to a copy of schema here
            schema = dict(schema)
            schema['deleted'] = {'type': 'bool', 'index': None}
            schema['ts_offset'] = {'type': 'int', 'index': None}

        # open heap files
        self.metaheap = MetaHeapFile(FILES_DIR+"/"+self.dbname+"/"+'metaheap', schema)
        self.tsheap = TSHeapFile(FILES_DIR+"/"+self.dbname+"/"+'tsheap', self.tsLength)

        self.pks = PKIndex(self.dbname)

        # DNY: to store fields that will have associated indexes
        self.indexFields = [field for field, value in self.schema.items()
                                  if value['index'] is not None]
        self.indexes = {}
        for field in self.indexFields:
            if (self.schema[field]['index']==2) and (len(self.schema[field]['values']) <= MAX_CARD):
                # TODO self.indexes[field] = BitMaskIndex()
                self.indexes[field] = TreeIndex(field, self.dbname)
            else:
                self.indexes[field] = TreeIndex(field, self.dbname)

    def __len__(self):
        "Dunder function to return length of timeseries db"
        return len(self.pks)

    def __getitem__(self,key):
        """Dunder function that returns all columns for this primary key
        """
        return self._get_meta_dict(key)

    def delete_database(self):
        """
        Remove the database.
        """
        #ASK: added close to fix files being open issue
        self.close()
        shutil.rmtree(self.data_dir)

    def close(self):
        self.metaheap.close()
        self.tsheap.close()
        self.pks.close()

    def _check_pk(self,pk):
        "Method to check that 'pk' is a string"
        try:
            assert isinstance(pk,str), "Invalid PK"
        except:
            raise ValueError('ts must be a timeseries.Timeseries object')

    def insert_ts(self, pk, ts):
        "Given a pk and a timeseries, insert them"
        self._check_pk(pk)
        if not isinstance(ts, timeseries.TimeSeries):
            raise ValueError('ts must be a timeseries.Timeseries object')
        if pk in self.pks:
            raise ValueError('Duplicate primary key found during insert')
        if len(ts) != self.tsLength:
            raise ValueError('TimeSeries must have length {}. Current length: {}'.format(self.tsLength, len(ts)))

        ts_offset = self.tsheap.encode_and_write_ts(ts) # write ts to tsheap file

        # DNY: write default meta values to disk
        meta = list(self.metaheap.fieldsDefaultValues)
        meta[self.metaheap.fields.index('ts_offset')] = ts_offset
        meta[self.metaheap.fields.index('ts_offset_set')] = True
        pk_offset = self.metaheap.encode_and_write_meta(meta)

        self.pks[pk] = pk_offset
        self.update_indices(pk)

    def _get_meta_list(self,pk):
        pk_offset = self.pks[pk]# DNY: temporary
        return self.metaheap.read_and_return_meta(pk_offset)

    def _get_meta_dict(self,pk):
        metaList = self._get_meta_list(pk)
        meta = {}
        for n, field in enumerate(self.metaheap.fields):
            if field in self.schema.keys():
                if self.schema[field]['type'] == "bool" or metaList[n+1]:
                    meta[field] = metaList[n]
        # ASK: this needs to contain the ts as well
        meta['ts'] = self._return_ts(pk)
        return meta

    def _return_ts(self,pk):
        # DNY: temporary testing function
        ts_offset = self._get_meta_list(pk)[self.metaheap.fields.index('ts_offset')]
        return self.tsheap.read_and_decode_ts(ts_offset)

    def upsert_meta(self, pk, new_meta):
        "Upsert metadata into the timeseries in the database."
        # TODO DNY: Does not support updating primary keys
        # TODO DNY: Does not support deleting metadata once inserted

        pk_offset = self.pks[pk]# DNY: temporary
        meta = self.metaheap.read_and_return_meta(pk_offset)
        old_meta_dict = self._get_meta_dict(pk)

        for n, field in enumerate(self.metaheap.fields):
            # will skip all the *_set entries
            if field in new_meta.keys():
                #TODO DNY: implement type/ error checking of the inserted values
                meta[n] = new_meta[field]
                if self.schema[field]['type'] != "bool":
                    meta[n+1] = True
        self.metaheap.encode_and_write_meta(meta, pk_offset)
        self.update_indices(pk, old_meta_dict)

    def index_bulk(self, pks=[]):
        if len(pks) == 0:
            pks = self.pks
        for pkid in pks:
            self.update_indices(pkid)

    def remove_indices(self, pk, old_meta_dict):
        """
        Remove the odl stored indices.

        Parameters
        ----------
        pk : int
            primary key
        old_meta_dict : dict
            old metadata dictionary
        """
        for field in self.indexes.keys():
            if field in old_meta_dict.keys():
                self.indexes[field].remove(old_meta_dict[field], pk)

    def update_indices(self, pk, old_meta_dict=None):
        "Update indices after a change has occurred. Eg. Called after insertion"
        if old_meta_dict is not None:
            self.remove_indices(pk, old_meta_dict)

        meta = self._get_meta_list(pk)
        for field in self.indexFields:
            field_idx = self.metaheap.fields.index(field)
            if self.schema[field]['type'] != "bool":
                # if value not set, skip
                if not meta[field_idx+1]:
                    continue
            self.indexes[field].insert(meta[field_idx],pk)

    def _getDataForRows(self,pks_out,fields_to_ret):
        "helper function to return appropriate data to user"
        data_list_out = []

        # just return primary_key and empty dicts
        if fields_to_ret is None:
            data_list_out = [{} for _ in range(len(pks_out))]

        # return all fields except for the 'ts' field
        elif fields_to_ret == []:
            for p in pks_out:
                values_dict = self._get_meta_dict(p)
                d = {field:value for field, value in values_dict.items() if field != 'ts'}
                d['pk'] = p
                data_list_out.append(d)

        # return all fields that the user has specified
        elif isinstance(fields_to_ret,list):
            for p in pks_out:
                values_dict = self._get_meta_dict(p)
                d = {field:value for field, value in values_dict.items() if field in fields_to_ret}
                if 'pk' in fields_to_ret:
                    d['pk'] = p
                data_list_out.append(d)

        # something went wrong
        else:
            raise Exception("Fields requested must be a list or None")

        return pks_out, data_list_out

    def select(self, meta, fields_to_ret=[], additional=None):
        """
        Select timeseries elements in the database that match the criteria set
        in meta.

        Parameters
        ----------
        metadata_dict: a dictionary object
            the selection criteria (filters)
        fields_to_ret: a list object
            If not `None`, only these fields of the timeseries are returned.
            Otherwise, the timeseries are returned.
        additional: a dictionary object
            additional computation to perform on the query matches before they're
            returned. You can sort or limit the number of results that you receive.
        """
        # Find matching keys
        pks_out = set(self.pks.keys())
        for field,criteria in meta.items():
            if field == 'pk':
                if criteria in self.pks:
                    pks_out = set([criteria])
                else:
                    return set()
            elif field in self.schema:
                # Range Query
                #DNY: TODO change BitmapIndex to contain 'get'
                if isinstance(criteria,dict):
                    op,val = list(criteria.items())[0]
                    matches = self.indexes[field].get(val,OPMAP[op])
                    pks_out = pks_out & set(matches)
                # Exact Query
                else:
                    # Index exists
                    if field in self.indexes:
                        matches = self.indexes[field].get(criteria)
                    # Index does not exist (shouldn't be called often)
                    else:
                        matches = []
                        for pk in self.pks:
                            test_meta = self._get_meta_dict[p]
                            if field in test_meta.keys() and test_meta[field] == criteria:
                                matches.append(pk)
                    pks_out = pks_out & set(matches)

        # Sort and Limit
        pks_out = list(pks_out)
        if additional and 'sort_by' in additional:
            sortfield = additional['sort_by'][1:]
            sortdir = additional['sort_by'][0]

            if sortfield not in self.schema:
                raise Exception("Sort Column not in schema")

            if sortdir == '+':
                pks_out = sorted(pks_out,key=lambda p: self._get_meta_dict(p)[sortfield])
            elif sortdir == '-':
                pks_out = sorted(pks_out,key=lambda p: self._get_meta_dict(p)[sortfield],reverse=True)
            else:
                raise Exception("Ill-defined sort order. Must be '+' or '-'")
        if additional and 'limit' in additional:
            amt = int(additional['limit'])
            if amt > len(pks_out):
                pks_out = pks_out[:amt]

        return self._getDataForRows(pks_out,fields_to_ret)
