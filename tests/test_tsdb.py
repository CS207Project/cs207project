import unittest
import timeseries as ts
from tsdb import TSDBClient

# TODO: (HWB) Automatically run server in background.
# TODO: (HWB) Abstract out set up for each test to make them truly independent.

client = TSDBClient()

class TSDBTests(unittest.TestCase):
    def test_insert1(self):
        print("\n", "insert1")
        status, payload = client.insert_ts('one',ts.TimeSeries([1, 2, 3],[1, 4, 9]))
        self.assertEqual(status.value, 0)

    def test_insert2(self):
        print("\n", "insert2")
        status, payload = client.insert_ts('two',ts.TimeSeries([2, 3, 4],[4, 9, 16]))
        self.assertEqual(status.value, 0)

    def test_insert3(self):
        print("\n", "insert3")
        status, payload = client.insert_ts('three',ts.TimeSeries([9,3,4],[4,0,16]))
        self.assertEqual(status.value, 0)

    def test_insert4(self):
        print("\n", "insert4")
        status, payload = client.insert_ts('four',ts.TimeSeries([0,0,4],[1,0,4]))
        self.assertEqual(status.value, 0)

    def test_insert5(self):
        print("\n", "insert5")
        status, payload = client.insert_ts('two',ts.TimeSeries([2, 3, 4],[4, 9, 16]))
        self.assertEqual(status.value, 3)

    def test_meta_upsert1(self):
        print("\n", "upsert1")
        status, payload = client.upsert_meta('one', {'order': 1, 'blarg': 1})
        self.assertEqual(status.value, 0)

    def test_meta_upsert2(self):
        print("\n", "upsert2")
        status, payload = client.upsert_meta('two', {'order': 2})
        self.assertEqual(status.value, 0)

    def test_meta_upsert3(self):
        print("\n", "upsert3")
        status, payload = client.upsert_meta('three', {'order': 1, 'blarg': 2})
        self.assertEqual(status.value, 0)

    def test_meta_upsert4(self):
        print("\n", "upsert4")
        status, payload = client.upsert_meta('four', {'order': 2, 'blarg': 2})
        self.assertEqual(status.value, 0)

    def test_select1(self):
        print("\n", "select1")
        status, payload = client.select()
        self.assertEqual((status.value, set(payload)), (0, set(['one', 'two', 'three', 'four'])))

    def test_select2(self):
        print("\n", "select2")
        status, payload = client.select({'order': 1})
        self.assertEqual((status.value, set(payload)), (0, set(['one', 'three'])))

    def test_select3(self):
        print("\n", "select3")
        status, payload = client.select({'blarg': 1})
        self.assertEqual((status.value, set(payload)), (0, set(['one'])))

    def test_select4(self):
        print("\n", "select4")
        status, payload = client.select({'order': 1, 'blarg': 2})
        self.assertEqual((status.value, set(payload)), (0, set(['three'])))
