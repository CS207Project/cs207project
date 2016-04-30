import asynctest
from unittest.mock import Mock
from tsdb import *
import timeseries as ts
import numpy as np
import asyncio
import time

class TSDBServerTest(asynctest.TestCase):

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
        self.server = TSDBServer(self.db)
        self.prot = TSDBProtocol(self.server)
        self.des = Deserializer()

        msg = TSDBOp_InsertTS('one', ts.TimeSeries([1,2,3],[1,4,9]))
        status, payload = self._mockSendingMessage(msg)

        msg = TSDBOp_InsertTS('two',ts.TimeSeries([2, 3, 4],[4, 9, 16]))
        status, payload = self._mockSendingMessage(msg)

        msg = TSDBOp_InsertTS('three',ts.TimeSeries([9,3,4],[4,0,16]))
        status, payload = self._mockSendingMessage(msg)

        msg = TSDBOp_InsertTS('four',ts.TimeSeries([0,0,4],[1,0,4]))
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
                # print("object!!!")
                # print(obj)
                status = obj['status']  # until proven otherwise.
                payload = obj['payload']  # until proven otherwise.
                break
        return status,payload

    async def test_add_trigger(self):

        msg = TSDBOp_AddTrigger('stats','insert_ts',['mean','sd'],None)
        status, payload =  self._mockSendingMessage(msg)

        msg = TSDBOp_InsertTS('five',ts.TimeSeries([0,0,4],[1,15,4]))
        status, payload = self._mockSendingMessage(msg)
        await asyncio.sleep(3)

        msg = TSDBOp_UpsertMeta('five', {'order': -1})
        status, payload =  self._mockSendingMessage(msg)

        msg = TSDBOp_Select({'pk': 'five'}, [], None)
        status, payload = self._mockSendingMessage(msg)
        self.assertEqual(payload['five']['mean'], np.mean([1,15,4]))

    async def test_remove_trigger(self):

        msg = TSDBOp_AddTrigger('stats','insert_ts',['mean','sd'],None)
        status, payload =  self._mockSendingMessage(msg)

        msg = TSDBOp_InsertTS('five',ts.TimeSeries([0,0,4],[1,15,4]))
        status, payload = self._mockSendingMessage(msg)
        await asyncio.sleep(3)

        msg = TSDBOp_Select({'pk': 'five'}, [], None)
        status, payload = self._mockSendingMessage(msg)
        self.assertEqual(payload['five']['mean'], np.mean([1,15,4]))

        msg = TSDBOp_RemoveTrigger('stats','insert_ts')
        status, payload =  self._mockSendingMessage(msg)
        await asyncio.sleep(3)

        msg = TSDBOp_InsertTS('six',ts.TimeSeries([0,0,4],[1,15,45]))
        status, payload = self._mockSendingMessage(msg)

        msg = TSDBOp_Select({'pk': 'six'}, [], None)
        status, payload = self._mockSendingMessage(msg)
        self.assertNotIn('mean',payload['six'])


if __name__ == '__main__':
    asynctest.main()
