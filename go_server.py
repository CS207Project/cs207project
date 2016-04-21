#!/usr/bin/env python3
from tsdb import TSDBServer, DictDB
import timeseries as ts

identity=lambda x:x
to_int=lambda x:int(x)
schema = {
  'pk': {'convert': identity, 'index': None},  #will be indexed anyways
  'ts': {'convert': identity, 'index': None},
  'order': {'convert': to_int, 'index': 1},
  'blarg': {'convert': to_int, 'index': 1},
  'useless': {'convert': identity, 'index': None},
  'mean': {'convert': identity, 'index': None},
  'std': {'convert': identity, 'index': None},
}

def main():
  db = DictDB(schema, 'pk')
  server = TSDBServer(db)
  server.run()

if __name__=='__main__':
  main()
