#!/usr/bin/env python3
from tsdb import TSDBServer, DictDB

identity = lambda x: x

#DNY: 'convert' is the function used to make the inputs the right type
schema = {
  'pk': {'convert': identity, 'index': None},
  'ts': {'convert': identity, 'index': None},
  'order': {'convert': int, 'index': 1},
  'blarg': {'convert': int, 'index': 1},
  'useless': {'convert': identity, 'index': None},
}


def main():
    db = DictDB(schema)
    server = TSDBServer(db)
    server.run()

if __name__ == '__main__':
    main()
