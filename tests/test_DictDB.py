import unittest
from tsdb import DictDB
import timeseries as ts
import numpy as np

class DictDBTests(unittest.TestCase):

    def setUp(self):
        identity = lambda x: x
        to_int = lambda x:int(x)
        to_float = lambda x:float(x)
        to_bool = lambda x:bool(x)

        schema = {
          'pk': {'convert': identity, 'index': None},  #will be indexed anyways
          'ts': {'convert': identity, 'index': None},
          'order': {'convert': to_int, 'index': 1},
          'blarg': {'convert': to_int, 'index': 1},
          'useless': {'convert': identity, 'index': None},
          'mean': {'convert': to_float, 'index': 1},
          'std': {'convert': to_float, 'index': 1},
          'vp': {'convert': to_bool, 'index': 1}
        }
        self.db = DictDB(schema,'pk',3)
        self.db.insert_ts('one',ts.TimeSeries([1, 2, 3],[1, 4, 9]))
        self.db.insert_ts('two',ts.TimeSeries([2, 3, 4],[4, 9, 16]))
        self.db.insert_ts('three',ts.TimeSeries([9,3,4],[4,0,16]))
        self.db.insert_ts('four',ts.TimeSeries([0,0,4],[1,0,4]))
        self.db.upsert_meta('one', {'order': 1, 'blarg': 1})
        self.db.upsert_meta('two', {'order': 2})
        self.db.upsert_meta('three', {'order': 1, 'blarg': 2})
        self.db.upsert_meta('four', {'order': 2, 'blarg': 2})

    def tearDown(self):
        pass

    def test_insert_duplicate(self):
        with self.assertRaises(ValueError):
            self.db.insert_ts('two',ts.TimeSeries([2, 3, 4],[4, 9, 16]))

    def test_insert_wronglen(self):
        with self.assertRaises(ValueError):
            self.db.insert_ts('nine',ts.TimeSeries([2, 3, 4, 5],[4, 9, 16, 25]))

    def test_select1(self):
        print("\n", "select1")
        pks, payload = self.db.select({},None,None)
        self.assertEqual(set(pks), set(['one', 'two', 'three', 'four']))

    def test_select2(self):
        print("\n", "select2")
        pks, payload = self.db.select({'order': 1},None,None)
        self.assertEqual(set(pks), set(['one', 'three']))

    def test_select3(self):
        print("\n", "select2")
        pks, payload = self.db.select({'order': 1},None,None)
        self.assertEqual(set(pks), set(['one', 'three']))

    def test_select4(self):
        print("\n", "select4")
        pks, payload = self.db.select({'order': 1, 'blarg': 2}, ['ts'], None)
        self.assertEqual(set(pks), set(['three']))
        self.assertEqual(payload[0]['ts'], ts.TimeSeries([9,3,4],[4,0,16]))

    def test_select5(self):
        pks, payload = self.db.select({'order': {'>': 1}, 'blarg': 2}, ['pk','blarg','order'], None)
        self.assertEqual(set(pks), set(['four']))
        self.assertEqual(set(payload[0].keys()), set(['pk','blarg','order']))

    def test_select6(self):
        pks, payload = self.db.select({'order': {'>': 1}}, [], None)
        self.assertEqual(set(pks), set(['two', 'four']))

        for p in payload:
            if p['pk'] == 'two':
                self.assertEqual(set(p.keys()), set(['pk','order']))
            if p['pk'] == 'four':
                self.assertEqual(set(p.keys()), set(['pk','order','blarg']))

    def test_select7(self):
        with self.assertRaises(Exception):
            pks, payload = self.db.select({'order': {'>': 1}}, [], {'sort_by':'order'})

    def test_select8(self):
        self.db.upsert_meta('four', {'order': 3, 'blarg': 2})

        pks, payload = self.db.select({'order': {'>': 1}}, [], {'sort_by':'+order'})
        self.assertEqual(pks, ['two', 'four'])

        pks, payload = self.db.select({'order': {'>': 1}}, [], {'sort_by':'-order'})
        self.assertEqual(pks, ['four', 'two'])

        self.db.upsert_meta('four', {'order': 2, 'blarg': 2})

    def test_select9(self):
        self.db.upsert_meta('four', {'order': 3, 'blarg': 2})

        pks, payload = self.db.select({'order': {'>': 1}}, [], {'sort_by':'+order',
                                                                'limit': 1})
        self.assertEqual(pks, ['two'])

        self.db.upsert_meta('four', {'order': 2, 'blarg': 2})

    def test_select10(self):
        self.db.upsert_meta('four', {'order': 3, 'blarg': 2})

        pks, payload = self.db.select({'order': {'>': 1}}, [], {'sort_by':'-order',
                                        'limit': 1,'blah':'nonsense'})
        self.assertEqual(pks, ['four'])

        self.db.upsert_meta('four', {'order': 2, 'blarg': 2})

    def test_del1(self):
        self.db.upsert_meta('four', {'order': 3, 'blarg': 2})
        self.db.delete_ts('four')

        pks, payload = self.db.select({'order': {'>': 1}}, [], {'sort_by':'-order',
                                        'limit': 1,'blah':'nonsense'})
        self.assertEqual(pks, ['two'])

        self.db.insert_ts('four',ts.TimeSeries([0,0,4],[1,0,4]))
        self.db.upsert_meta('four', {'order': 2, 'blarg': 2})

    def test_del2(self):
        self.db.delete_ts('one')
        self.db.delete_ts('two')
        self.db.delete_ts('three')
        self.db.delete_ts('four')

        pks, payload = self.db.select({},None,None)
        self.assertEqual(set(pks), set([]))

        self.db.insert_ts('one',ts.TimeSeries([1, 2, 3],[1, 4, 9]))
        self.db.insert_ts('two',ts.TimeSeries([2, 3, 4],[4, 9, 16]))
        self.db.insert_ts('three',ts.TimeSeries([9,3,4],[4,0,16]))
        self.db.insert_ts('four',ts.TimeSeries([0,0,4],[1,0,4]))
        self.db.upsert_meta('one', {'order': 1, 'blarg': 1})
        self.db.upsert_meta('two', {'order': 2})
        self.db.upsert_meta('three', {'order': 1, 'blarg': 2})
        self.db.upsert_meta('four', {'order': 2, 'blarg': 2})

    def test_del3(self):
        with self.assertRaises(ValueError):
            self.db.delete_ts('five')

    def test_select11(self):
        with self.assertRaises(Exception):
            pks, payload = self.db.select({'order': {'>': 1}}, [], {'sort_by':'+order',
                                                            'limit':'a'})

if __name__ == '__main__':
    unittest.main()
