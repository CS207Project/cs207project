#!/usr/bin/env python3
from tsdb import TSDBServer, PersistantDB, FILES_DIR
import timeseries as ts
import numpy as np
from scipy.stats import norm
import os

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

persistantSchema = {
  'pk':    {'type': 'string', 'index': None},  #will be indexed anyways
  'ts':    {'type': None,     'index': None}, #DNY: TimeSeries has no type
  'order': {'type': 'int',    'index': 2,    'values': [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]},
  'blarg': {'type': 'int',    'index': 2,    'values': [1, 2]},
  'mean':  {'type': 'float',  'index': 1},
  'std':   {'type': 'float',  'index': 1},
  'vp':    {'type': 'bool',   'index': 2,    'values': [0,1]},
  'd-vp1': {'type': 'float',  'index': 1}
}#DNY: in the persistantdb, I will add categories for deleted ts and offsets
# in the tsheap file
# entries in TSDB are strongly typed

# One thought I had was to use a numpy array and associating that with a stored,
# temporally ordered list of primary keys. Then, if a primary key is updated, i
# can simply change the array, and if a new key comes in, I can add it to the
# list and add a new element onto the back of the array. Is that a good way

TS_LENGTH = 1024
NUMVPS = 5

def main():
    # we augment the schema by adding columns for 5 vantage points
    # for i in range(NUMVPS):
    #     schema["d_vp-{}".format(i)] = {'convert': float, 'index': 1}


    db = PersistantDB(persistantSchema, pk_field='pk', db_name='test', ts_length=TS_LENGTH)
    # ts_samp = ts.TimeSeries(list(range(1024)),list(range(1024)))
    # meta_ex, ts_ex = tsmaker(1024)
    # meta_ex2, ts_ex2 = tsmaker(1024)

    # db.insert_ts('testperm', ts_samp)
    # db.insert_ts('test34', ts_ex)
    # check that the default values were set
    # print(db.metaheap.fields)
    # meta = db._return_meta('test')
    #print(meta)#check that these are default value

    # check that the stored timeseries is the same
    # read_ts = db._return_ts('test34')
    # print(ts_ex)
    # print(read_ts)

    # assert(ts_ex == read_ts)

    # check that the new values are set
    # db.upsert_meta('test34', meta_ex)
    # print(db.metaheap.fields)
    # print(meta_ex)
    # meta = db._return_meta('test34')
    # for field in meta_ex.keys():
    #     assert(meta_ex[field]==meta[db.metaheap.fields.index(field)])

    # db.insert_ts('test2', ts_ex)
    # print(db._read_and_return_meta('test2'))
    # db.upsert_meta('test2', meta_ex2)
    # print(db._read_and_return_meta('test2'))

    # server = TSDBServer(db)
    # server.run()

def tsmaker(n):
    "returns metadata and a time series in the shape of a jittered normal"
    meta={}
    meta['order'] = int(np.random.choice([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]))
    # meta['blarg'] = int(np.random.choice([1, 2]))
    meta['mean'] = 10**np.random.randn()
    meta['std'] = 10**np.random.randn()
    meta['vp'] = np.random.choice([True, False])
    meta['d-vp1'] = 10**np.random.randn()
    t = np.linspace(0.0,1.0,n)
    v = norm.pdf(t, meta['mean'], meta['std']) + meta['std']*np.random.randn(n)
    return meta, ts.TimeSeries(t, v)


if __name__=='__main__':
    main()
