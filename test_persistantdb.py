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
  'order': {'type': 'int',    'index': 1},
  'blarg': {'type': 'int',    'index': 1},
  'mean':  {'type': 'float',  'index': 1},
  'std':   {'type': 'float',  'index': 1},
  'vp':    {'type': 'bool',   'index': 1},
  'd-vp1': {'type': 'float',  'index': 1}
}#DNY: in the persistantdb, I will add categories for deleted ts and offsets
# in the tsheap file
# entries in TSDB are strongly typed

TS_LENGTH = 1024
NUMVPS = 5

def main():
    # we augment the schema by adding columns for 5 vantage points
    # for i in range(NUMVPS):
    #     schema["d_vp-{}".format(i)] = {'convert': float, 'index': 1}


    db = PersistantDB(persistantSchema, pk_field='pk', db_name='test', ts_length=TS_LENGTH)
    meta_ex, ts_ex = tsmaker(1024)
    meta_ex2, ts_ex2 = tsmaker(1024)

    db.insert_ts('test', ts_ex)
    # check that the default values were set
    print(db.metaFields)
    print(db._read_and_return_meta('test'))

    # check that the stored timeseries is the same
    offset = db._read_and_return_meta('test')[db.metaFields.index('ts_offset')]
    print(ts_ex)
    read_ts = db._read_and_decode_ts(offset)
    print(read_ts)
    print(ts_ex == read_ts)

    # check that the new values are set
    db.upsert_meta('test', meta_ex)
    print(db.metaFields)
    print(meta_ex)
    print(db._read_and_return_meta('test'))

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
