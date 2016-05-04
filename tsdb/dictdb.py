"""A dictionary based in-memory version of the time series database
"""
from .baseclasses import BaseDB
from collections import defaultdict
from operator import and_
from functools import reduce
import operator
import numbers

# this dictionary will help you in writing a generic select operation
OPMAP = {
    '<': operator.lt,
    '>': operator.gt,
    '==': operator.eq,
    '!=': operator.ne,
    '<=': operator.le,
    '>=': operator.ge
}

class DictDB(BaseDB):
    """
    A database implementation in a dictionary

    Attributes
    ----------
    indexes :
        a default dict of primary keys and offsets in file of the values
    rows :
        contains the rows of data. Each entry points to a dictionary
    schema :
        the schema that the dictionary follows
    pkfield :
        selects the field to be considered as the primary key. Defaults to `pk`.
    ts_length :
        lenght of the timeseries. Defaults to 100.
    """
    def __init__(self, schema, pk_field = 'pk', ts_length = 100):
        """
        A database implementation in a dictionary

        Parameters
        ----------
        schema : dict object
            the schema that the database follows (fields, converts, indexes, etc.)
        pkfield : string
            primary key field. Defaults to `pk`.
        ts_length : int
            lenght of timeseries. Defaults to 100.
        """
        self.indexes = {}
        self.rows = {} # contains the row data, each entry points to another dictionary
        self.schema = schema # DNY: see go_server.py for example schema
        self.pkfield = pk_field
        self.ts_length = ts_length
        for s in schema:
            indexinfo = schema[s]['index']
            # convert = schema[s]['convert']
            # later use binary search trees for highcard/numeric
            # bitmaps for lowcard/str_or_factor
            if indexinfo is not None:
                self.indexes[s] = defaultdict(set)# create an index for every non-None schema

    def __getitem__(self,key):
        """Dunder method to get the the values at a given row"""
        if key in self.rows:
            return self.rows[key]
        else:
            raise ValueError("primary_key not in the database: "+ str(key))

    def __setitem__(self):
        raise NotImplementedError

    def insert_ts(self, pk, ts):
        "Given a pk and a timeseries, insert them"
        print("in db insert",pk,ts)
        if len(ts) != self.ts_length:
            raise ValueError('TimeSeries is of the wrong length. Should be '+ str(self.ts_length))
        if pk not in self.rows:
            self.rows[pk] = {'pk': pk}
        else:
            raise ValueError('Duplicate primary key found during insert')
        self.rows[pk]['ts'] = ts
        self.update_indices(pk)

    def delete_ts(self,pk):
        "Given a pk, remove that timeseries from the database"
        raise NotImplementedError

    def upsert_meta(self, pk, meta):
        """
        Given a primary key and a dict of meta fields, value pairs, upsert
        them as long as they're in the schema.
        """
        #DNY written
        # assume meta is a dict, field->values
        for field, value in meta.items():
            if field in self.schema:# ignore all fields not in schema
                if pk not in self.rows:# assert that timeseries already exists
                    raise ValueError('Primary key not found in database')
                fieldConvert = self.schema[field]['convert']
                self.rows[pk][field] = fieldConvert(value)
        self.update_indices(pk)

    def index_bulk(self, pks=[]):
        if len(pks) == 0:
            pks = self.rows
        for pkid in pks:#DNY: I think this was a mistake. formerly 'self.pks:'
            self.update_indices(pkid)

    def update_indices(self, pk):
        "Update indices after a change has occurred. Eg. Called after insertion"
        row = self.rows[pk]
        for field in row:#DNY: eg 'pk' or 'ts', or any entry in self.schema
            v = row[field]
            if self.schema[field]['index'] is not None:
                idx = self.indexes[field]# idx is a defaultdict(set)
                idx[v].add(pk)#DNY: 'v' must be hashable

    #ASK: Helper func
    def _getDataForRows(self,pks_out,fields_to_ret):
        data_list_out = []

        # just return primary_key and empty dicts
        if fields_to_ret is None:
            data_list_out = [{} for _ in range(len(pks_out))]

        # return all fields except for the 'ts' field
        elif fields_to_ret == []:
            for p in pks_out:
                values_dict = self.rows[p]
                data_list_out.append(
                    {field:value for field,value in values_dict.items() if field != 'ts'})

        # return all fields that the user has specified
        elif isinstance(fields_to_ret,list):
            for p in pks_out:
                values_dict = self.rows[p]
                data_list_out.append(
                    {field:value for field,value in values_dict.items() if field in fields_to_ret})

        # something went wrong
        else:
            raise Exception("Fields requested must be a list or None")

        return pks_out, data_list_out

    def select(self, meta, fields_to_ret, additional):
        """
        Select timeseries elements in the database that match the criteria set
        in metadata_dict.

        Parameters
        ----------
        meta: a dictionary object
            the selection criteria (filters)
        fields_to_ret: a dictionary object
            If not `None`, only these fields of the timeseries are returned.
            Otherwise, the timeseries are returned.
        additional: a dictionary object
            additional computation to perform on the query matches before they're
            returned. You can sort or limit the number of results that you receive.
        """
        pks_out = set(self.rows.keys())

        for field,criteria in meta.items():
            if field in self.schema:
                fieldConvert = self.schema[field]['convert']

                #ASK: this is a range query. Not sure how to do this with indices with
                #     current implementation
                if(isinstance(criteria,dict)):
                    op,val = list(criteria.items())[0]
                    matches = [p for p in pks_out if field in self.rows[p] and
                                    OPMAP[op](self.rows[p][field],fieldConvert(val))]
                    pks_out = pks_out & set(matches)

                #ASK: this is an exact query
                else:
                    criteria = fieldConvert(criteria) #ASK: convert to the right format

                    #ASK: we have an index for this field
                    if field in self.indexes:
                        matches = self.indexes[field][criteria]

                    #ASK: we don't have an index for this field
                    else:
                        matches = [p for p in pks_out if field in self.rows[p] and
                                    self.rows[p][field] == criteria]
                    pks_out = pks_out & set(matches)

        #ASK: decide what to return
        pks_out = list(pks_out)
        if additional and 'sort_by' in additional:
            # print("Sorting by ",additional['sort_by'][1:]," in direction ",additional['sort_by'][0])
            sortfield = additional['sort_by'][1:]
            sortdir = additional['sort_by'][0]

            if sortfield not in self.schema:
                raise Exception("Sort Column not in schema")

            if sortdir == '+':
                pks_out = sorted(pks_out,key=lambda p: self.rows[p][sortfield])
            elif sortdir == '-':
                pks_out = sorted(pks_out,key=lambda p: self.rows[p][sortfield],reverse=True)
            else:
                raise Exception("Illdefined sort order. Must be '+' or '-'")

        if additional and 'limit' in additional:
            pks_out = pks_out[:int(additional['limit'])]

        return self._getDataForRows(pks_out,fields_to_ret)
