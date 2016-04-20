from collections import defaultdict
from operator import and_
from functools import reduce
import operator
import numbers

# this dictionary will help you in writing a generic select operation
OPMAP = {
    '<': operator.lt,
    '>': operator.le,
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

    #ASK Helper func
    #TODO: use indices when possible
    def _getDataForRows(self,pks_out,fields_to_ret):
        # if fields is None: return only pks
        # like so [pk1,pk2],[{},{}]
        # if fields is [], this means all fields
        #except for the 'ts' field. Looks like
        #['pk1',...],[{'f1':v1, 'f2':v2},...]
        # if the names of fields are given in the list, include only those fields. `ts` ia an
        #acceptable field and can be used to just return time series.
        #see tsdb_server to see how this return
        #value is used
        # return pks, matchedfielddicts

        if fields_to_ret is None:
            return list(pks_out),[{} for _ in range(len(pks_out))]
        elif fields_to_ret == []:
            return list(pks_out), [{field:value for field,value in values_dict.items() if field != 'ts'}
                    for p,values_dict in self.rows.items() if p in pks_out]
        elif isinstance(fields_to_ret,list):
            return list(pks_out), [{field:value for field,value in values_dict.items() if field in fields_to_ret}
                        for p,values_dict in self.rows.items() if p in pks_out]
        else:
            raise Exception("Fields requested must be a list or None")

    def select(self, meta, fields_to_ret):
        # if fields is None: return only pks
        # like so [pk1,pk2],[{},{}]
        # if fields is [], this means all fields
        #except for the 'ts' field. Looks like
        #['pk1',...],[{'f1':v1, 'f2':v2},...]
        # if the names of fields are given in the list, include only those fields. `ts` ia an
        #acceptable field and can be used to just return time series.
        #see tsdb_server to see how this return
        #value is used
        # return pks, matchedfielddicts

        #ASK: Implementing via a full table scan right now
        pks_out = set(self.rows.keys())
        for field,criteria in meta.items():
            if field in self.schema:
                fieldConvert = self.schema[field]['convert']
                if(isinstance(criteria,dict)): #ASK: this is a range query
                    op,val = list(criteria.items())[0]
                    matches = [p for p in pks_out if field in self.rows[p] and
                                    OPMAP[op](self.rows[p][field],fieldConvert(val))]
                    pks_out = pks_out & set(matches)
                elif(isinstance(criteria,numbers.Real)): #ASK: this is an exact query
                    matches = [p for p in pks_out if field in self.rows[p] and
                                self.rows[p][field] == fieldConvert(criteria)]
                    pks_out = pks_out & set(matches)

        #ASK: decide what to return
        return self._getDataForRows(pks_out,fields_to_ret)
