from collections import defaultdict
from operator import and_
from functools import reduce


class DictDB:
    "Database implementation in a dict"
    def __init__(self, schema):
        "initializes database with indexed and schema"
        self.indexes = {}
        self.rows = {} # contains the row data, each entry points to another dictionary
        self.schema = schema # DNY: see go_server.py for example schema
        self.pkfield = 'pk'
        for s in schema:
            indexinfo = schema[s]['index']
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

    def select(self, meta):
        #implement select, AND'ing over the filters in the md metadata dict
        #remember that each item in the dictionary looks like key==value
        #DNY written
        pks = set(self.rows.keys())
        for field, value in meta.items():
            if field in self.schema:
                pks = pks & self.indexes[field][value]
        # json_dict = {}
        # for key in pks:
        #     json_dict[key] = self.rows[key]
        return list(pks)#json_dict
