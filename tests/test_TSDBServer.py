import unittest
from unittest.mock import Mock
from tsdb import *
import timeseries as ts
import numpy as np
import asyncio
import time

class TSDBServerTest(unittest.TestCase):

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
          'vp': {'convert': to_bool, 'index': 1},
          'vp_num': {'convert': to_int, 'index': 1},
          'd_vp-1': {'convert': float, 'index': 1}
        }
        self.db = DictDB(schema,'pk',3)
        self.server = TSDBServer(self.db)
        self.prot = TSDBProtocol(self.server)
        self.des = Deserializer()

        msg = TSDBOp_AddTrigger('corr','insert_ts',['d_vp-1'],ts.TimeSeries([1,2,3],[1,4,9]))
        status, payload =  self._mockSendingMessage(msg)

        msg = TSDBOp_InsertTS('one', ts.TimeSeries([1, 2, 3],[1,4,9]))
        status, payload = self._mockSendingMessage(msg)

        msg = TSDBOp_UpsertMeta('one', {'vp': True, 'vp_num': 1})
        status, payload =  self._mockSendingMessage(msg)

        msg = TSDBOp_InsertTS('two',ts.TimeSeries([1, 2, 3],[4, 9, 16]))
        status, payload = self._mockSendingMessage(msg)

        msg = TSDBOp_InsertTS('three',ts.TimeSeries([1, 2, 3],[4,0,16]))
        status, payload = self._mockSendingMessage(msg)

        msg = TSDBOp_InsertTS('four',ts.TimeSeries([1, 2, 3],[1,0,4]))
        status, payload = self._mockSendingMessage(msg)

    def tearDown(self):
        pass

    def _mockSendingMessage(self,msg):
        w = Mock(spec=asyncio.WriteTransport)
        self.prot.conn = w
        self.prot.data_received(serialize(msg.to_json()))

        for method, args, _ in w.method_calls:
            if method == 'write':
                self.des.append(args[0])
                decodedResponse  = self.des.deserialize()
                obj = TSDBOp_Return.from_json(decodedResponse)
                print("object!!!")
                print(obj)
                status = obj['status']  # until proven otherwise.
                payload = obj['payload']  # until proven otherwise.
                break
        return status,payload

    def test_upsert_meta1(self):
        msg = TSDBOp_UpsertMeta('one', {'order': 1, 'blarg': 1})
        status, payload =  self._mockSendingMessage(msg)
        self.assertIs(payload,None)

    def test_upsert_meta2(self):
        msg = TSDBOp_UpsertMeta('two', {'order': 2})
        status, payload =  self._mockSendingMessage(msg)
        self.assertIs(payload,None)

    def test_upsert_meta3(self):
        msg = TSDBOp_UpsertMeta('three', {'order': 1, 'blarg': 2})
        status, payload =  self._mockSendingMessage(msg)
        self.assertIs(payload,None)

    def test_upsert_meta4(self):
        msg = TSDBOp_UpsertMeta('four', {'order': 2, 'blarg': 2})
        status, payload =  self._mockSendingMessage(msg)
        self.assertIs(payload,None)

    def test_insert_duplicate(self):
        msg = TSDBOp_InsertTS('two',ts.TimeSeries([2, 3, 4],[4, 34, 16]))
        status, payload = self._mockSendingMessage(msg)
        self.assertEqual(status,TSDBStatus.INVALID_KEY)

    def test_del1(self):
        msg = TSDBOp_DeleteTS('two')
        status, payload = self._mockSendingMessage(msg)

        msg = TSDBOp_UpsertMeta('four', {'order': 3, 'blarg': 2})
        status, payload =  self._mockSendingMessage(msg)

        msg = TSDBOp_Select({'order': {'>': 1}}, [], {'sort_by':'+order'})
        status, payload = self._mockSendingMessage(msg)
        self.assertEqual(list(payload.keys()), ['four'])

        msg = TSDBOp_InsertTS('two',ts.TimeSeries([2, 3, 4],[4, 9, 16]))
        status, payload = self._mockSendingMessage(msg)

        msg = TSDBOp_UpsertMeta('four', {'order': 2, 'blarg': 2})
        status, payload =  self._mockSendingMessage(msg)

    def test_augmented_select(self):

        msg = TSDBOp_UpsertMeta('two', {'order': 2})
        status, payload =  self._mockSendingMessage(msg)

        msg = TSDBOp_UpsertMeta('four', {'order': 3, 'blarg': 2})
        status, payload =  self._mockSendingMessage(msg)

        msg = TSDBOp_AugmentedSelect('stats',['m','sd'],None,{'order': {'>': 1}},None)
        status, payload =  self._mockSendingMessage(msg)

        self.assertEqual(payload['four']['m'], np.mean([1,0,4]))
        self.assertEqual(payload['four']['sd'], np.std([1,0,4]))

        self.assertEqual(payload['two']['m'], np.mean([4, 9, 16]))
        self.assertEqual(payload['two']['sd'], np.std([4, 9, 16]))

    def test_find_similar1(self):

        query = ts.TimeSeries([1, 2, 3],[4, 0, 3])
        msg = TSDBOp_FindSimilar(query)
        status, payload =  self._mockSendingMessage(msg)

        near = list(payload.keys())[0]
        self.assertTrue(near in ['one','two','three','four'])

    def test_find_similar2(self):

        query = ts.TimeSeries([0, 5, 10],[15, 25, 50])
        msg = TSDBOp_FindSimilar(query)
        status, payload =  self._mockSendingMessage(msg)

        near = list(payload.keys())[0]
        self.assertTrue(near in ['one','two','three','four'])

class TSDBServerTest2(unittest.TestCase):

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
          'vp': {'convert': to_bool, 'index': 1},
          'vp_num': {'convert': to_int, 'index': 1},
          'd_vp-1': {'convert': float, 'index': 1}
        }
        self.db = DictDB(schema,'pk',3)
        self.server = TSDBServer(self.db)
        self.prot = TSDBProtocol(self.server)
        self.des = Deserializer()

        msg = TSDBOp_AddTrigger('corr','insert_ts',['d_vp-1'],ts.TimeSeries([1,2,3],[1,4,9]))
        status, payload =  self._mockSendingMessage(msg)

        msg = TSDBOp_InsertTS('one', ts.TimeSeries([1, 2, 3],[1,4,9]))
        status, payload = self._mockSendingMessage(msg)

        msg = TSDBOp_UpsertMeta('one', {'vp': True, 'vp_num': 1})
        status, payload =  self._mockSendingMessage(msg)

        msg = TSDBOp_InsertTS('two',ts.TimeSeries([1, 2, 3],[4, 9, 16]))
        status, payload = self._mockSendingMessage(msg)

        msg = TSDBOp_InsertTS('three',ts.TimeSeries([1, 2, 3],[4,0,16]))
        status, payload = self._mockSendingMessage(msg)

        msg = TSDBOp_InsertTS('four',ts.TimeSeries([1, 2, 3],[1,0,4]))
        status, payload = self._mockSendingMessage(msg)

        msg = TSDBOp_UpsertMeta('one', {'order': 1, 'blarg': 1})
        status, payload =  self._mockSendingMessage(msg)

        msg = TSDBOp_UpsertMeta('two', {'order': 2})
        status, payload =  self._mockSendingMessage(msg)

        msg = TSDBOp_UpsertMeta('three', {'order': 1, 'blarg': 2})
        status, payload =  self._mockSendingMessage(msg)

        msg = TSDBOp_UpsertMeta('four', {'order': 2, 'blarg': 2})
        status, payload =  self._mockSendingMessage(msg)

    def tearDown(self):
        pass

    def _mockSendingMessage(self,msg):
        w = Mock(spec=asyncio.WriteTransport)
        self.prot.conn = w
        self.prot.data_received(serialize(msg.to_json()))

        for method, args, _ in w.method_calls:
            if method == 'write':
                self.des.append(args[0])
                decodedResponse  = self.des.deserialize()
                obj = TSDBOp_Return.from_json(decodedResponse)
                print("object!!!")
                print(obj)
                status = obj['status']  # until proven otherwise.
                payload = obj['payload']  # until proven otherwise.
                break
        return status,payload

    def test_select1(self):
        msg = TSDBOp_Select({},[],None)
        # msg = {}
        # msg['op'] = 'select'
        # msg['md'] = metadata_dict
        status, payload =  self._mockSendingMessage(msg)
        # print("\n\n")
        # print(payload)
        pks = payload.keys()
        self.assertEqual(set(pks), set(['one', 'two', 'three', 'four']))

    def test_select2(self):
        msg = TSDBOp_Select({'order': 1},None,None)
        status, payload = self._mockSendingMessage(msg)
        # print("\n\n")
        # print(payload)
        pks = payload.keys()
        self.assertEqual(set(pks), set(['one', 'three']))

    def test_select3(self):
        msg = TSDBOp_Select({'order': 1},None,None)
        status, payload = self._mockSendingMessage(msg)
        self.assertEqual(set(payload.keys()), set(['one', 'three']))

    def test_select4(self):
        msg = TSDBOp_Select({'order': 1, 'blarg': 2}, ['ts'], None)
        status, payload = self._mockSendingMessage(msg)
        self.assertEqual(set(payload.keys()), set(['three']))

    def test_select5(self):
        msg = TSDBOp_Select({'order': {'>': 1}, 'blarg': 2}, ['pk','blarg','order'], None)
        status, payload = self._mockSendingMessage(msg)
        self.assertEqual(set(payload.keys()), set(['four']))

    def test_select6(self):
        msg = TSDBOp_Select({'order': {'>': 1}}, [], None)
        status, payload = self._mockSendingMessage(msg)
        self.assertEqual(set(payload.keys()), set(['two', 'four']))

    def test_select7(self):
        msg = TSDBOp_UpsertMeta('four', {'order': 3, 'blarg': 2})
        self._mockSendingMessage(msg)
        msg = TSDBOp_Select({'order': {'>': 1}}, [], {'sort_by':'+order', 'limit': 1})
        status, payload = self._mockSendingMessage(msg)

        self.assertEqual(set(payload.keys()), set(['two']))

        msg = TSDBOp_UpsertMeta('four', {'order': 2, 'blarg': 2})
        self._mockSendingMessage(msg)

    def test_select8(self):
        msg = TSDBOp_UpsertMeta('two', {'order': 2})
        status, payload =  self._mockSendingMessage(msg)

        msg = TSDBOp_UpsertMeta('four', {'order': 3, 'blarg': 2})
        status, payload =  self._mockSendingMessage(msg)

        msg = TSDBOp_Select({'order': {'>': 1}}, [], {'sort_by':'+order'})
        status, payload = self._mockSendingMessage(msg)
        self.assertEqual(list(payload.keys()), ['two', 'four'])

        msg = TSDBOp_Select({'order': {'>': 1}}, [], {'sort_by':'-order'})
        status, payload = self._mockSendingMessage(msg)
        self.assertEqual(list(payload.keys()), ['four','two'])

        msg = TSDBOp_UpsertMeta('four', {'order': 2, 'blarg': 2})
        status, payload =  self._mockSendingMessage(msg)

if __name__ == '__main__':
    unittest.main()
