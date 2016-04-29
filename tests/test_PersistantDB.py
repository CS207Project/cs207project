import unittest
from tsdb import PersistantDB
import os
import timeseries as ts
import numpy as np

class PersistantDBTests(unittest.TestCase):
    def setUp(self):
        self.dirPath = "files/testing"
        if not os.path.isdir(self.dirPath):
            os.makedirs(self.dirPath)
            self._createdDirs = True
        else:
            self._createdDirs = False

        schema = {
          'pk':    {'type': 'string', 'index': None},
          'ts':    {'type': None,     'index': None},
          'order': {'type': 'int',    'index': 2,    'values': [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]},
          'blarg': {'type': 'int',    'index': 2,    'values': [1, 2]},
          'mean':  {'type': 'float',  'index': 1},
          'std':   {'type': 'float',  'index': 1},
          'vp':    {'type': 'bool',   'index': 2,    'values': [0,1]},
          'd-vp1': {'type': 'float',  'index': 1}
        }

        self.schema = schema

        self.tsLength = 1024

        self.db = PersistantDB(schema, pk_field='pk', db_name='testing', ts_length=self.tsLength, testing=True)

        for i in range(100):
            pk = 'ts-'+str(i)
            values = np.array(range(self.tsLength)) + i
            series = ts.TimeSeries(values, values)
            meta = {}
            n_order = len(schema['order']['values'])# 11
            meta['order'] = schema['order']['values'][i % n_order]
            n_blarg = 2
            meta['blarg'] = schema['blarg']['values'][i % n_blarg]
            meta['mean'] = series.mean()
            meta['std'] = series.std()
            meta['vp'] = False
            self.db.insert_ts(pk, series)
            self.db.upsert_meta(pk, meta)

    def tearDown(self):
        self.db.delete_database()

    def test_meta_save_ts(self):
        self.db.close()
        self.db = PersistantDB(pk_field='pk', db_name='testing', ts_length=self.tsLength, testing=True)
        self.assertEqual(len(self.db),100)

    def test_schema_change_good(self):
        self.db.close()
        self.db = PersistantDB(self.schema, pk_field='pk', db_name='testing', ts_length=self.tsLength, testing=True)

    def test_schema_change_bad(self):
        badschema = dict(self.schema)
        badschema['blarg'] = {'type': 'int',    'index': 2,    'values': [1, 2, 3]}
        self.db.close()
        with self.assertRaises(ValueError):
            self.db = PersistantDB(badschema, pk_field='pk', db_name='testing', ts_length=self.tsLength, testing=True)

    def test_bad_insert(self):
        pk = 'bad'
        with self.assertRaises(ValueError):
            bad_series = np.array(range(self.tsLength+3))
            self.db.insert_ts(pk, bad_series)
        with self.assertRaises(ValueError):
            values = np.array(range(self.tsLength+5))
            bad_series = ts.TimeSeries(values, values)
            self.db.insert_ts(pk, bad_series)

    def test_read_meta(self):
        for i in range(100):
            pk = 'ts-'+str(i)
            values = np.array(range(self.tsLength)) + i
            series = ts.TimeSeries(values, values)
            r_meta = self.db._get_meta_list(pk)
            n_order = len(self.schema['order']['values'])# 11
            assert(r_meta[self.db.metaheap.fields.index('order')] == self.schema['order']['values'][i % n_order])
            n_blarg = 2
            assert(r_meta[self.db.metaheap.fields.index('blarg')] == self.schema['blarg']['values'][i % n_blarg])
            assert(r_meta[self.db.metaheap.fields.index('mean')] == series.mean())
            assert(r_meta[self.db.metaheap.fields.index('std')] == series.std())

    def test_read_ts(self):
        for i in range(100):
            pk = 'ts-'+str(i)
            values = np.array(range(self.tsLength)) + i
            series = ts.TimeSeries(values, values)
            r_ts = self.db._return_ts(pk)
            assert(series == r_ts)

    def test_select(self):
        self.db.select({'pk':'ts-0'})
        self.db.select({'pk':'ts-35'})
        self.db.select({'order':2})
        self.db.select({'order':{'>=':2}},['blarg'],{'sort_by':'+blarg'})
        # TODO Need to add in tests to trip the associated errors here

    # TODO : Need to test indexing functions
    # def test_(self):
    #     pass
    #
    # def test_(self):
    #     pass
