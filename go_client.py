#!/usr/bin/env python3
from tsdb import TSDBClient
import timeseries as ts

def main():
    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    client = TSDBClient()

    #ppl = open('standardize.ppl').read()
    client.add_trigger('junk', 'insert_ts', None, 23)#DNY: looks for junk.py in procs/ directory
    #DNY: not targeting anything here
    #client.add_trigger('junk', 'select', None, 23)
    client.add_trigger('stats', 'insert_ts', ['mean', 'std'], None)

    client.insert_ts('one',ts.TimeSeries([1, 2, 3],[1, 4, 9]))
    client.insert_ts('two',ts.TimeSeries([2, 3, 4],[4, 9, 16]))
    client.insert_ts('three',ts.TimeSeries([9,3,4],[4,0,16]))

    client.remove_trigger('junk', 'insert_ts')
    client.insert_ts('four',ts.TimeSeries([0,0,4],[1,0,4]))

    client.upsert_meta('one', {'order': 1, 'blarg': 1})
    client.upsert_meta('two', {'order': 2})
    client.upsert_meta('three', {'order': 1, 'blarg': 2})
    client.upsert_meta('four', {'order': 2, 'blarg': 2})
    print("UPSERTS FINISHED")
    print('---------------------')
    client.select()
    print('---------------------')
    client.select(fields=['order'])
    print('---------------------')
    client.select(fields=[])
    print('---------------------')
    print('---------------------')
    client.select({'order': 1}, fields=['ts'])
    print('{{{{{{{{{{{{{{}}}}}}}}}}}}}}')
    client.select({'blarg': 1}, fields=[])
    print('{{{{{{{{{{{{{{}}}}}}}}}}}}}}')
    bla = client.select({'order': 1, 'blarg': 2})
    print("END", bla)
    client.select({'blarg': {'>=': 2}}, fields=['blarg', 'mean'])
    client.select({'blarg': {'>=': 2}, 'order': 1}, fields=['blarg', 'std', 'order'])
    #client.add_pipeline(ppl)
    #client.autokey('useless','print', None)

if __name__=='__main__':
    main()
