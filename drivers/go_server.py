#!/usr/bin/env python3
from tsdb import TSDBServer, DictDB
import timeseries as ts

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
    for i in range(NUMVPS):
        schema["d_vp-{}".format(i)] = {'convert': float, 'index': 1}
    db = DictDB(schema, 'pk')
    server = TSDBServer(db)
    server.run()

if __name__=='__main__':
    main()