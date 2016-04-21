from socket import *
import time
from .tsdb_serialization import serialize, LENGTH_FIELD_LENGTH, Deserializer
from .tsdb_ops import *
from .tsdb_error import *

class TSDBClient(object):
    """
    The client. This could be used in a python program, web server, or REPL!
    """
    def __init__(self, port=9999):
        self.port = port
        self.deserializer = Deserializer()

    def insert_ts(self, primary_key, ts):
        # your code here, construct from the code in tsdb_ops.py
        msg = TSDBOp_InsertTS(primary_key, ts)
        # msg = {}
        # msg['op'] = 'insert_ts'
        # msg['pk'] = primary_key
        # msg['ts'] = [ts.values, ts.times]
        self._send(msg.to_json())

    def upsert_meta(self, primary_key, metadata_dict):
        # your code here
        msg = TSDBOp_UpsertMeta(primary_key, metadata_dict)
        # msg = {}
        # msg['op'] = 'upsert_meta'
        # msg['pk'] = primary_key
        # msg['md'] = metadata_dict
        self._send(msg.to_json())

    def select(self, metadata_dict={}, fields=None):
        #DNY: TODO, need to redo
        msg = TSDBOp_Select(metadata_dict,fields)
        # msg = {}
        # msg['op'] = 'select'
        # msg['md'] = metadata_dict
        status, payload =  self._send(msg.to_json())
        return TSDBStatus(status), payload

    def add_trigger(self, proc, onwhat, target, arg):
        msg = TSDBOp_AddTrigger(proc,onwhat,target,arg)

        status, payload =  self._send(msg.to_json())
        return TSDBStatus(status), payload

    def remove_trigger(self, proc, onwhat):
        msg = TSDBOp_RemoveTrigger(proc,onwhat)

        status, payload =  self._send(msg.to_json())
        return TSDBStatus(status), payload

    # Feel free to change this to be completely synchronous
    # from here onwards. Return the status and the payload
    def _send(self, msg):
        # ASK: changing to synchronous
        RECV_SIZE = 8192

        # connect and send
        s = socket(AF_INET,SOCK_STREAM)
        s.connect(('',self.port))
        s.send(serialize(msg))

        # receive
        while True:
            response = s.recv(RECV_SIZE)
            if not response:
                break
            self.deserializer.append(response)

        s.close() #close the socket

        print('-----------')
        print('C> writing')

        #DNY: now looking at tsdb_server.py for how to deserialize
        if self.deserializer.ready():# it should always be ready, or the read failed
            decodedResponse = self.deserializer.deserialize()
            # print("decodedResponse!!!")
            # print(decodedResponse)
            obj = TSDBOp_Return.from_json(decodedResponse)
            # print("object!!!")
            # print(obj)
            status = obj['status']  # until proven otherwise.
            payload = obj['payload']  # until proven otherwise.
            print('C> status:',str(TSDBStatus(status)))
            print('C> payload:',payload)
            return status, payload
        else:
            raise(ValueError("client failed to read the full response"))

        return status,payload
