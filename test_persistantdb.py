#!/usr/bin/env python3
from tsdb import TSDBServer, PersistantDB, FILES_DIR
import timeseries as ts
import numpy as np
from scipy.stats import norm
import os

schema = {
  'pk':    {'type': 'string', 'index': None},  #will be indexed anyways
  'ts':    {'type': None,     'index': None}, #DNY: TimeSeries has no type
  'order': {'type': 'int',    'index': 2,    'values': [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]},
  'blarg': {'type': 'int',    'index': 2,    'values': [1, 2]},
  'mean':  {'type': 'float',  'index': 1},
  'std':   {'type': 'float',  'index': 1},
  'vp':    {'type': 'bool',   'index': 2,    'values': [0,1]},
  'd-vp1': {'type': 'float',  'index': 1}
}

TS_LENGTH = 1024
NUMVPS = 5

from tsdb import PersistantDB
db = PersistantDB(db_name='daniel')
db.select({'pk':'ts-0'})
db.select({'pk':'ts-35'})
db.select({'order':2})
db.select({'order':{'>=':2}},['blarg'])

def main():
    # we augment the schema by adding columns for 5 vantage points
    # for i in range(NUMVPS):
    #     schema["d_vp-{}".format(i)] = {'convert': float, 'index': 1}
    db = PersistantDB(db_name='daniel')
    db.select({'pk':'ts-35'})
    db.select({'order':2})
    db.select({'order':{'>=':2}},['blarg'])
    # db = PersistantDB(schema, pk_field='pk', db_name='daniel', ts_length=TS_LENGTH)
    # ts_samp = ts.TimeSeries(list(range(1024)),list(range(1024)))
    # meta_ex, ts_ex = tsmaker(1024)
    # meta_ex2, ts_ex2 = tsmaker(1024)

    # db.insert_ts('testperm', ts_samp)

    # for i in range(100):
    #     pk = 'ts-'+str(i)
    #     values = np.array(range(TS_LENGTH)) + i
    #     series = ts.TimeSeries(values, values)
    #     meta = {}
    #     n_order = len(schema['order']['values'])# 11
    #     meta['order'] = schema['order']['values'][i % n_order]
    #     n_blarg = 2
    #     meta['blarg'] = schema['blarg']['values'][i % n_blarg]
    #     meta['mean'] = series.mean()
    #     meta['std'] = series.std()
    #     meta['vp'] = False
    #     db.insert_ts(pk, series)
    #     db.upsert_meta(pk, meta)


    # db.select({'order':0})

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
