"""Time Series Database Client: This could be used in a python program, web server, or REPL!
"""
import asyncio
from .tsdb_serialization import serialize, LENGTH_FIELD_LENGTH, Deserializer
from .tsdb_ops import *
from .tsdb_error import *

class TSDBClient(object):
    """
    The client. This could be used in a python program, web server, or REPL!

    Attributes
    ----------
    port :
        the port with which to connect to the server
    """
    def __init__(self, port=9999):
        """Instantiate a TSDBClient class object

        Parameters
        ----------
        port : int
            the port with which to connect to the server. Default is 9999.
        """
        self.port = port
        self.deserializer = Deserializer()

    async def insert_ts(self, primary_key, ts):
        """
        Send the server a request to insert a timeseries into the database.

        Parameters
        ----------
        `primary_key`: int
            a unique identifier for the timeseries
        `ts`: a TimeSeries object
            the timeseries, an instance of the `TimeSeries` class
        """
        # your code here, construct from the code in tsdb_ops.py
        msg = TSDBOp_InsertTS(primary_key, ts)
        # msg = {}
        # msg['op'] = 'insert_ts'
        # msg['pk'] = primary_key
        # msg['ts'] = [ts.values, ts.times]
        status, payload =  await self._send(msg.to_json())
        return TSDBStatus(status), payload

    async def delete_ts(self, primary_key):
        """
        Send the server a request to delete a timeseries from the database.

        Parameters
        ----------
        `primary_key`: int
            a unique identifier for the timeseries
        """
        # your code here, construct from the code in tsdb_ops.py
        msg = TSDBOp_DeleteTS(primary_key)
        # msg = {}
        # msg['op'] = 'insert_ts'
        # msg['pk'] = primary_key
        # msg['ts'] = [ts.values, ts.times]
        status, payload =  await self._send(msg.to_json())
        return TSDBStatus(status), payload

    async def upsert_meta(self, primary_key, metadata_dict):
        """
        Send the server a request to upsert metadata into the timeseries in
        the database.

        Parameters
        ----------
        `primary_key`: int
            a unique identifier for the timeseries
        `metadata_dict`: a dictionary object
            the metadata to upsert into the timeseries
        """
        # your code here
        msg = TSDBOp_UpsertMeta(primary_key, metadata_dict)
        # msg = {}
        # msg['op'] = 'upsert_meta'
        # msg['pk'] = primary_key
        # msg['md'] = metadata_dict
        status, payload =  await self._send(msg.to_json())
        return TSDBStatus(status), payload

    async def select(self, metadata_dict={}, fields=None, additional=None):
        """
        Send the server a request for the selection of timeseries elements in
        the database that match the criteria set in metadata_dict.

        Parameters
        ----------
        metadata_dict: a dictionary object
            the selection criteria (filters)
        fields: a dictionary object
            If not `None`, only these fields of the timeseries are returned.
            Otherwise, the timeseries are returned.
        additional: a dictionary object
            additional computation to perform on the query matches before they're
            returned. You can sort or limit the number of results that you receive.
        """
        #DNY: TODO, need to redo
        msg = TSDBOp_Select(metadata_dict,fields,additional)
        # msg = {}
        # msg['op'] = 'select'
        # msg['md'] = metadata_dict
        status, payload =  await self._send(msg.to_json())
        return TSDBStatus(status), payload

    async def augmented_select(self, proc, target, arg=None, metadata_dict={}, additional=None):
        """
        Send the server a request for the selection of timeseries elements in
        the database that match the criteria set in metadata_dict and then run a
        stored procedure on that result

        Parameters
        ----------
        proc : string
            name of the stored procedure that will be run on the results
        metadata_dict: a dictionary object
            the selection criteria (filters)
        additional: a dictionary object
            additional computation to perform on the query matches before they're
            returned. You can sort or limit the number of results that you receive.
        target : list
            what the results of the stored procedure will be stored in
        """
        msg = TSDBOp_AugmentedSelect(proc,target,arg,metadata_dict,additional)
        status, payload =  await self._send(msg.to_json())
        return TSDBStatus(status), payload

    async def find_similar(self, arg):
        """Send the server a request to find the closest ts to this one

        Parameters
        ----------

        arg : TimeSeries
            reference time series
        """
        msg = TSDBOp_FindSimilar(arg)
        status, payload =  await self._send(msg.to_json())
        return TSDBStatus(status), payload

    async def make_vp_tree(self):
        """Make a Vantage Point Tree given the current state of the database
        """
        msg = TSDBOp_MakeVPTree()
        status, payload =  await self._send(msg.to_json())
        return TSDBStatus(status), payload

    async def add_trigger(self, proc, onwhat, target, arg):
        """
        Send the server a request to add a trigger.

        Parameters
        ----------
        `proc` : which of the modules in procs. Options: 'corr', 'junk', 'stats'
        `onwhat` : the trigger
        `target` : metadata to be upserted
        `arg` : additional argument
        """
        msg = TSDBOp_AddTrigger(proc,onwhat,target,arg)

        status, payload =  await self._send(msg.to_json())
        return TSDBStatus(status), payload

    async def remove_trigger(self, proc, onwhat):
        msg = TSDBOp_RemoveTrigger(proc,onwhat)

        status, payload =  await self._send(msg.to_json())
        return TSDBStatus(status), payload

    # Feel free to change this to be completely synchronous
    # from here onwards. Return the status and the payload
    async def _send_coro(self, msg, loop):
        # your code here
        # DNY: looking heavily at the sockets lecture
        reader, writer = await asyncio.open_connection('localhost',self.port,loop=loop)
        print('-----------')
        print('C> writing')
        writer.write(serialize(msg))
        await writer.drain() #ASK : make sure buffer is flushed i.e everything is written
        response = await reader.read()
        writer.close()# close the connection once the response is read

        #DNY: now looking at tsdb_server.py for how to deserialize
        self.deserializer.append(response)
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

    #call `_send` with a well formed message to send.
    #once again replace this function if appropriate
    async def _send(self, msg):
        loop = asyncio.get_event_loop()
        #coro = asyncio.ensure_future(self._send_coro(msg, loop))
        #DNY: coro is a Task object from asyncio
        #loop.run_until_complete(coro)#DNY: blocking call until coro completes
        return await self._send_coro(msg, loop)
