#!/usr/bin/env python3
""" This is a utility file that starts a dictionary based in-memory database
with a given timeseries length and a given number of vantage points.
It is meant to be an example of how to start our system and also
servers as a way for us to test our code.

Takes two arguments:
    -len : length of timeseries
    -vps : number of vantage points

IF YOU EDIT THIS FILE TESTS MIGHT BREAK. IT IS MEANT AS A DEMO ONLY.
"""

from tsdb import TSDBServer, DictDB
import timeseries as ts
import argparse
import sys

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

TS_LENGTH = 100
NUMVPS = 5

def main():
    # we augment the schema by adding columns for 5 vantage points
    for i in range(NUMVPS):
        schema["d_vp-{}".format(i)] = {'convert': float, 'index': 1}
    db = DictDB(schema, 'pk',TS_LENGTH)
    server = TSDBServer(db)
    server.run()

if __name__=='__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-len', help="length of timeseies",
                        type=int,default=TS_LENGTH,required=False)
    parser.add_argument('-vps', help="number of vantage points",
                        type=int,default=NUMVPS,required=False)
    args = parser.parse_args(sys.argv[1:])

    TS_LENGTH = args.len
    NUMVPS = args.vps

    main()
