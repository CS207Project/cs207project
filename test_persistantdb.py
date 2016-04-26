#!/usr/bin/env python3
from tsdb import TSDBServer, PersistantDB, FILES_DIR
import timeseries as ts
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

TS_LENGTH = 1024
NUMVPS = 5

def main():
    # we augment the schema by adding columns for 5 vantage points
    # for i in range(NUMVPS):
    #     schema["d_vp-{}".format(i)] = {'convert': float, 'index': 1}
    if not os.path.exists(FILES_DIR):
        os.makedirs(FILES_DIR)

    db = PersistantDB(schema, pk_field='pk', db_name='test', ts_length=TS_LENGTH)
    # server = TSDBServer(db)
    # server.run()

def tsmaker(m, s, j):
    "returns metadata and a time series in the shape of a jittered normal"
    meta={}
    meta['order'] = int(np.random.choice([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]))
    meta['blarg'] = int(np.random.choice([1, 2]))
    t = np.arange(0.0, 1.0, 0.01)
    v = norm.pdf(t, m, s) + j*np.random.randn(100)
    return meta, ts.TimeSeries(t, v)


if __name__=='__main__':
    main()
