"""Time Series Database Server: Owns any version of a database and communicates with the TSDBClient
"""

import asyncio
from .dictdb import DictDB
from importlib import import_module
from collections import defaultdict, OrderedDict
from .tsdb_serialization import Deserializer, serialize
from .tsdb_error import *
from .tsdb_ops import *
import procs
import time
<<<<<<< HEAD
import vptrees
=======
from .vptrees import *
>>>>>>> bdb6e427d24eaaccc1845ef9dcf536086ce1f8bc

def trigger_callback_maker(pk, target, calltomake):
    def callback_(future):
        result = future.result()
        if target is not None:
            calltomake(pk, dict(zip(target, result)))
        return result
    return callback_

class TSDBProtocol(asyncio.Protocol):
    #DNY: see https://docs.python.org/3/library/asyncio-protocol.html#asyncio-protocol
    def __init__(self, server): #DNY: presumably given TSDBServer as input
        self.server = server
        self.deserializer = Deserializer()# comes from tsdb_serialization.py
        self.futures = []

    def _insert_ts(self, op):
        """
        Insert a timeseries into the database.

        Parameters
        ----------
        op : a TSDBOp object
            contains the primary key and timeseries to insert
        """
        self.server.db.insert_ts(op['pk'], op['ts'])
        self._run_trigger('insert_ts', [op['pk']])
        return TSDBOp_Return(TSDBStatus.OK, op['op'])

    def _delete_ts(self, op):
        """
        Delete a timeseies from the database.

        Parameters
        ----------
        op : a TSDBOp object
            contains the primary key to delete
        """
        self.server.db.delete_ts(op['pk'])
        self._run_trigger('delete_ts', [op['pk']])
        return TSDBOp_Return(TSDBStatus.OK, op['op'])

    def _upsert_meta(self, op):
        """
        Upsert metadata into a timeseries on the database.

        Parameters
        ----------
        op : a TSDBOp object
            contains the primary key and metadata dict (`op[md]`) to upsert
        """
        self.server.db.upsert_meta(op['pk'], op['md'])
        self._run_trigger('upsert_meta', [op['pk']])
        return TSDBOp_Return(TSDBStatus.OK, op['op'])

    def _select(self, op):
        """
        Select timeseries from the database.

        Parameters
        ----------
        op : a TSDBOp object
            contains metadata specifications (`op[md]`) to match in the query. Also
            contains fields of the matched timeseries to return. If left to
            default value of `None`, everything is returned.
        """
        loids, fields = self.server.db.select(op['md'], op['fields'], op['additional'])
        self._run_trigger('select', loids)
        if fields is not None:
            d = OrderedDict(zip(loids, fields))
            return TSDBOp_Return(TSDBStatus.OK, op['op'], d)
        else:
            d = OrderedDict((k,{}) for k in loids)
            return TSDBOp_Return(TSDBStatus.OK, op['op'], d)


    def _augmented_select(self, op):
        """
        Run a select and then synchronously run some computation on it

        Parameters
        ----------
        op : a TSDBOp object
            contains metadata specifications (`op[md]`) to match in the query. Also
            contains fields of the matched timeseries (`op[fields]`) to return.
            If left to default value of `None`, everything is returned.

            Additional elements are:
                `op[proc]` : module in proc to run
                `op[arg]` : an additional argument
                `op[target]` : will return targets mapped to return values of `op[proc]`
        """
        loids, fields = self.server.db.select(op['md'], None, op['additional'])
        print("Aug Select :: Select retured {} rows".format(len(loids)))

        proc = op['proc']  # the module in procs
        arg = op['arg']  # an additional argument, could be a constant
        target = op['target'] #not used to upsert any more, but rather to
        # return results in a dictionary with the targets mapped to the return
        # values from proc_main
        results=[]
        for pk in loids:
            row = self.server.db[pk]
            result = self.server._run_proc(proc, pk, row, arg)
            results.append(dict(zip(target, result)))
        return TSDBOp_Return(TSDBStatus.OK, op['op'], dict(zip(loids, results)))

    def _find_similar(self, op):
        """
        Find the most similar timeseies to the given timeseies from the database

        If Vantage Point trees are implemented this will change.
        Parameters
        ----------
        op : a TSDBOp object
            contains a query timeseries (`op[arg]`)
        """
        arg = op['arg']

        if self.server.vptree is not None:
            # find the right subgroup within the tree and compute distance to
            # all the points within it
            loids = self.server.vptree.getCloseSubset(arg, self.server._dist_vp_arg)

            results={}
            for pk in loids:
                row = self.server.db[pk]
                results[pk] = self.server._run_proc('corr', pk, row, arg)[0]

            # find the smallest distance amongst this ( or k smallest)
            n = min(results.keys(),key=lambda p: results[p])

            return TSDBOp_Return(TSDBStatus.OK, op['op'], {n:results[n]})

        else:
            vpkeys, _ = self.server.db.select({'vp': True}, None, {'sort_by' : '+vp_num'})

            # compute distance to all vps
            vpdist = {}
            for v in vpkeys:
                row = self.server.db[v]
                vpdist[v] = self.server._run_proc('corr', v, row, arg)[0]
                # time.sleep(1)

            #choose the lowest distance vantage point
            closest_vpk = min(vpkeys,key=lambda v:vpdist[v])
            closest_vpk_dist_col = 'd_vp-' + str(vpkeys.index(closest_vpk))
            # print(closest_vpk,closest_vpk_dist_col)


            # find all time series within 2*d(query, nearest_vp_to_query)
            # this is an augmented select to the same proc in correlation
            md = {closest_vpk_dist_col: {'<=': 2*vpdist[closest_vpk]}}
            loids, fields = self.server.db.select(md, None, None)

            print("Find Similar :: Select retured {} rows".format(len(loids)))

            # find distances to all timeseries within this circle around the Vantage
            # Point
            results={}
            for pk in loids:
                row = self.server.db[pk]
                results[pk] = self.server._run_proc('corr', pk, row, arg)[0]

            # find the smallest distance amongst this ( or k smallest)
            n = min(results.keys(),key=lambda p: results[p])

            return TSDBOp_Return(TSDBStatus.OK, op['op'], {n:results[n]})

    def _add_trigger(self, op):#DNY: Trigger is "if something happens, run this particular process", similar to a stored procedure.
        """
        Send the server a request to add a trigger.

        Parameters
        ----------
        `op[proc]` : which of the modules in procs. Options: 'corr', 'junk', 'stats'
        `op[onwha]t` : the trigger
        `op[target]` : metadata to be upserted
        `op[arg]` : additional argument
        """
        trigger_proc = op['proc']  # the module in procs DNY: proc = 'process', should be an async co-routine
        # see procs/ directory, at the same level as tsdb
        trigger_onwhat = op['onwhat']  # on what operation? eg `insert_ts`
        trigger_target = op['target']  # if provided, this meta will be upserted
        trigger_arg = op['arg']  # an additional argument, could be a constant
        # FIXME: this import should have error handling
        mod = import_module('procs.'+trigger_proc)
        storedproc = getattr(mod,'main')
        self.server.triggers[trigger_onwhat].append((trigger_proc, storedproc, trigger_arg, trigger_target))
        return TSDBOp_Return(TSDBStatus.OK, op['op'])

    def _remove_trigger(self, op):
        trigger_proc = op['proc']
        trigger_onwhat = op['onwhat']
        trigs = self.server.triggers[trigger_onwhat]
        for t in trigs:
            if t[0]==trigger_proc:
                trigs.remove(t)
        return TSDBOp_Return(TSDBStatus.OK, op['op'])

    def _run_trigger(self, opname, rowmatch):
        lot = self.server.triggers[opname]
        print("S> list of triggers to run", lot)
        for tname, t, arg, target in lot:
            for pk in rowmatch:
                row = self.server.db[pk]
                task = asyncio.ensure_future(t(pk, row, arg))
                task.add_done_callback(trigger_callback_maker(pk, target, self.server.db.upsert_meta))

    def _make_vp_tree(self, op):
        # get all the pks
        pks, fields = self.server.db.select({},['vp'],None)
        vps = [p for p,d in zip(pks, fields) if d['vp']]
        # print("pks", pks)
        # print("vps", vps)
        self.server.vptree = vptrees.VPTree(pks, vps, self.server._dist_vp_pks)
        return TSDBOp_Return(TSDBStatus.OK, op['op'])

    def connection_made(self, conn):
        "Connection established"
        print('S> connection made')
        #connection or transport is saved as an instance variable
        self.conn = conn#DNY: conn is a 'asyncio.WriteTransport' object
        #DNY: handles communication channels

    def data_received(self, data):
        print("------------------------------------------------")
        print('S> data received ['+str(len(data))+']: '+str(data))
        self.deserializer.append(data)#DNY: presumably deserializer handles readying data
        if self.deserializer.ready():
            msg = self.deserializer.deserialize()
            status = TSDBStatus.OK  # until proven otherwise.
            response = TSDBOp_Return(status, None)  # until proven otherwise.
            try:
                op = TSDBOp.from_json(msg)#DNY: constructs appropriate TSDBOp_... by identifying msg

                if isinstance(op, TSDBOp_InsertTS):
                    response = self._insert_ts(op)
                elif isinstance(op, TSDBOp_UpsertMeta):
                    response = self._upsert_meta(op)
                elif isinstance(op, TSDBOp_Select):
                    response = self._select(op)
                elif isinstance(op, TSDBOp_AugmentedSelect):
                    response = self._augmented_select(op)
                elif isinstance(op, TSDBOp_AddTrigger):
                    response = self._add_trigger(op)
                elif isinstance(op, TSDBOp_RemoveTrigger):
                    response = self._remove_trigger(op)
                elif isinstance(op, TSDBOp_DeleteTS):
                    response = self._delete_ts(op)
                elif isinstance(op, TSDBOp_FindSimilar):
                    response = self._find_similar(op)
                elif isinstance(op, TSDBOp_MakeVPTree):
                    response = self._make_vp_tree(op)
                else:
                    response = TSDBOp_Return(TSDBStatus.UNKNOWN_ERROR, op['op'])
            except Exception as e:
                print("Exception Occured")
                print(str(e.args))

                if len(e.args) > 0 and isinstance(e.args[0],TSDBStatus):
                    status = e.args[0]
                    response = TSDBOp_Return(status, list(e.args[1:]))
                else:
                    status = TSDBStatus.INVALID_OPERATION
                    response = TSDBOp_Return(status, list(e.args))
            finally:
                self.conn.write(serialize(response.to_json()))
                self.conn.close()

    def connection_lost(self, transport):
        print('S> connection lost')


class TSDBServer(object):
    """
    The server. This accepts requests from the client, processes them, and
    dispatches a response.

    Attributes
    ----------
    port :
        the port with which to connect to the server
    db :
        database engine
    triggers :
        a default dict of triggers
    """
    def __init__(self, db, port=9999):
        """
        Instantiate an instance of the server. This accepts requests from the
        client, processes them, and dispatches a response.

        Parameters
        ----------
        port : int
            port to listen on. Defaults to 9999.
        db : a DictDB
            database engine
        """
        self.port = port
        self.db = db
        self.triggers = defaultdict(list)
        self.autokeys = {}
        self.vptree = None

    def _dist_vp_pks(self, vp, pks):

        # get the info on this vp
        row = self.db[vp]

        # get the distance to all other keys
        dist_col = 'd_vp-'+str(row['vp_num'])
        loids, fields = self.db.select({},[dist_col],None)

        return [fields[loids.index(p)][dist_col] for p in pks]

    def _dist_vp_arg(self, vp, arg):

        # get the info on this vp
        row = self.db[vp]
        d = self._run_proc('corr', vp, row, arg)[0]
        return d

    def _run_proc(self, proc, pk, row, arg):
        mod = import_module('procs.'+proc)
        storedproc = getattr(mod,'proc_main')
        return storedproc(pk, row, arg)

    def exception_handler(self, loop, context):
        print('S> EXCEPTION:', str(context))
        loop.stop()

    def run(self):
        "Run the server."
        loop = asyncio.get_event_loop()
        # NOTE: enable this if you'd rather have the server stop on an error
        #       currently it dumps the protocol and keeps going; new connections
        #       are unaffected. Rather nice, actually.
        #loop.set_exception_handler(self.exception_handler)
        self.listener = loop.create_server(lambda: TSDBProtocol(self), '127.0.0.1', self.port)
        print('S> Starting TSDB server on port',self.port)
        listener = loop.run_until_complete(self.listener)
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            print('S> Exiting.')
        except Exception as e:
            print('S> Exception:',e)
        finally:
            listener.close()
            loop.close()


if __name__=='__main__':
    empty_schema = {'pk': {'convert': lambda x: x, 'index': None}}
    db = DictDB(empty_schema, 'pk')
    TSDBServer(db).run()
