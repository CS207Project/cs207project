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

class DictDB:
    "Database implementation in a dict"
    def __init__(self, schema,pk_field = 'pk'):
        "initializes database with indexed and schema"
        self.indexes = {}
        self.rows = {} # contains the row data, each entry points to another dictionary
        self.schema = schema # DNY: see go_server.py for example schema
        self.pkfield = pk_field
        for s in schema:
            indexinfo = schema[s]['index']
            # convert = schema[s]['convert']
            # later use binary search trees for highcard/numeric
            # bitmaps for lowcard/str_or_factor
            if indexinfo is not None:
                self.indexes[s] = defaultdict(set)# create an index for every non-None schema

    def insert_ts(self, pk, ts):
        "given a pk and a timeseries, insert them"
        print("in db insert",pk,ts)
        if pk not in self.rows:
            self.rows[pk] = {'pk': pk}
        else:
            raise ValueError('Duplicate primary key found during insert')
        self.rows[pk]['ts'] = ts
        self.update_indices(pk)

    def upsert_meta(self, pk, meta):
        "implement upserting field values, as long as the fields are in the schema."
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
        #ASK: Implementing via a full table scan right now

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
            print("Limiting")
            pks_out = pks_out[:int(additional['limit'])]

        return self._getDataForRows(pks_out,fields_to_ret)
