```
(py35)➜  cs207project git:(simpler) ✗ sh both.sh
Generating LALR tables
S> Starting TSDB server on port 9999
Generating LALR tables
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
S> connection made
S> data received [91]: b'[\x00\x00\x00{"op": "add_trigger", "arg": 23, "onwhat": "insert_ts", "target": null, "proc": "junk"}'
S> connection lost
C> status: TSDBStatus.OK
C> payload: None
-----------
C> writing
S> connection made
S> data received [105]: b'i\x00\x00\x00{"op": "add_trigger", "arg": null, "onwhat": "insert_ts", "target": ["mean", "std"], "proc": "stats"}'
S> connection lost
C> status: TSDBStatus.OK
C> payload: None
-----------
C> writing
S> connection made
S> data received [66]: b'B\x00\x00\x00{"op": "insert_ts", "ts": [[1, 2, 3], [1, 4, 9]], "pk": "one"}'
S> list of triggers to run [('junk', <function main at 0x103ae16a8>, 23, None), ('stats', <function main at 0x103ae1730>, None, ['mean', 'std'])]
[[[[[[[[[[[JUNKY]]]]]]]]]]]] one {'ts': <timeseries.timeseries.TimeSeries object at 0x103aef2e8>, 'pk': 'one'} 23
[[[[[[[[[[[STATS]]]]]]]]]]]] one {'ts': <timeseries.timeseries.TimeSeries object at 0x103aef2e8>, 'pk': 'one'} None
C> status: TSDBStatus.OK
C> payload: None
-----------
C> writing
S> connection lost
S> connection made
S> data received [67]: b'C\x00\x00\x00{"op": "insert_ts", "ts": [[2, 3, 4], [4, 9, 16]], "pk": "two"}'
S> list of triggers to run [('junk', <function main at 0x103ae16a8>, 23, None), ('stats', <function main at 0x103ae1730>, None, ['mean', 'std'])]
[[[[[[[[[[[JUNKY]]]]]]]]]]]] two {'ts': <timeseries.timeseries.TimeSeries object at 0x103aef4a8>, 'pk': 'two'} 23
[[[[[[[[[[[STATS]]]]]]]]]]]] two {'ts': <timeseries.timeseries.TimeSeries object at 0x103aef4a8>, 'pk': 'two'} None
C> status: TSDBStatus.OK
C> payload: None
-----------
C> writing
S> connection lost
S> connection made
S> data received [69]: b'E\x00\x00\x00{"op": "insert_ts", "ts": [[9, 3, 4], [4, 0, 16]], "pk": "three"}'
S> list of triggers to run [('junk', <function main at 0x103ae16a8>, 23, None), ('stats', <function main at 0x103ae1730>, None, ['mean', 'std'])]
[[[[[[[[[[[JUNKY]]]]]]]]]]]] three {'ts': <timeseries.timeseries.TimeSeries object at 0x103aef908>, 'pk': 'three'} 23
[[[[[[[[[[[STATS]]]]]]]]]]]] three {'ts': <timeseries.timeseries.TimeSeries object at 0x103aef908>, 'pk': 'three'} None
C> status: TSDBStatus.OK
C> payload: None
-----------
C> writing
S> connection lost
S> connection made
S> data received [67]: b'C\x00\x00\x00{"op": "remove_trigger", "onwhat": "insert_ts", "proc": "junk"}'
S> connection lost
C> status: TSDBStatus.OK
C> payload: None
-----------
C> writing
S> connection made
S> data received [67]: b'C\x00\x00\x00{"op": "insert_ts", "ts": [[0, 0, 4], [1, 0, 4]], "pk": "four"}'
S> list of triggers to run [('stats', <function main at 0x103ae1730>, None, ['mean', 'std'])]
[[[[[[[[[[[STATS]]]]]]]]]]]] four {'ts': <timeseries.timeseries.TimeSeries object at 0x103aef860>, 'pk': 'four'} None
S> connection lost
C> status: TSDBStatus.OK
C> payload: None
-----------
C> writing
C> msg {'op': 'upsert_meta', 'pk': 'one', 'md': {'order': 1, 'blarg': 1}}
S> connection made
S> data received [70]: b'F\x00\x00\x00{"op": "upsert_meta", "pk": "one", "md": {"order": 1, "blarg": 1}}'
S> D> ROW {'order': 1, 'blarg': 1, 'ts': <timeseries.timeseries.TimeSeries object at 0x103aef2e8>, 'pk': 'one'}
S> list of triggers to run []
S> connection lost
C> status: TSDBStatus.OK
C> payload: None
-----------
C> writing
C> msg {'op': 'upsert_meta', 'pk': 'two', 'md': {'order': 2}}
S> connection made
S> data received [58]: b':\x00\x00\x00{"op": "upsert_meta", "pk": "two", "md": {"order": 2}}'
S> D> ROW {'order': 2, 'ts': <timeseries.timeseries.TimeSeries object at 0x103aef4a8>, 'pk': 'two'}
S> list of triggers to run []
S> connection lost
C> status: TSDBStatus.OK
C> payload: None
-----------
C> writing
C> msg {'op': 'upsert_meta', 'pk': 'three', 'md': {'order': 1, 'blarg': 2}}
S> connection made
S> data received [72]: b'H\x00\x00\x00{"op": "upsert_meta", "pk": "three", "md": {"order": 1, "blarg": 2}}'
S> D> ROW {'order': 1, 'blarg': 2, 'ts': <timeseries.timeseries.TimeSeries object at 0x103aef908>, 'pk': 'three'}
S> list of triggers to run []
S> connection lost
C> status: TSDBStatus.OK
C> payload: None
-----------
C> writing
C> msg {'op': 'upsert_meta', 'pk': 'four', 'md': {'order': 2, 'blarg': 2}}
S> connection made
S> data received [71]: b'G\x00\x00\x00{"op": "upsert_meta", "pk": "four", "md": {"order": 2, "blarg": 2}}'
S> D> ROW {'order': 2, 'blarg': 2, 'ts': <timeseries.timeseries.TimeSeries object at 0x103aef860>, 'pk': 'four'}
S> list of triggers to run []
S> connection lost
C> status: TSDBStatus.OK
C> payload: None
-----------
C> writing
UPSERTS FINISHED
---------------------
S> connection made
S> data received [46]: b'.\x00\x00\x00{"op": "select", "fields": null, "md": {}}'
S> D> NO FIELDS
S> list of triggers to run []
S> connection lost
C> status: TSDBStatus.OK
C> payload: {'two': {}, 'three': {}, 'four': {}, 'one': {}}
-----------
C> writing
---------------------
S> connection made
S> data received [51]: b'3\x00\x00\x00{"op": "select", "fields": ["order"], "md": {}}'
S> D> FIELDS ['order'] ['three', 'two', 'one', 'four']
S> list of triggers to run []
S> connection lost
C> status: TSDBStatus.OK
C> payload: {'two': {'order': 2}, 'three': {'order': 1}, 'four': {'order': 2}, 'one': {'order': 1}}
-----------
C> writing
---------------------
S> connection made
S> data received [44]: b',\x00\x00\x00{"op": "select", "fields": [], "md": {}}'
S> D> ALL FIELDS
S> list of triggers to run []
S> connection lost
C> status: TSDBStatus.OK
C> payload: {'two': {'pk': 'two', 'order': 2}, 'three': {'blarg': 2, 'order': 1, 'pk': 'three'}, 'four': {'blarg': 2, 'order': 2, 'pk': 'four'}, 'one': {'blarg': 1, 'order': 1, 'pk': 'one'}}
-----------
C> writing
---------------------
---------------------
S> connection made
S> data received [58]: b':\x00\x00\x00{"op": "select", "fields": ["ts"], "md": {"order": 1}}'
S> D> FIELDS ['ts'] ['one', 'three']
S> list of triggers to run []
S> connection lost
C> status: TSDBStatus.OK
C> payload: {'three': {'ts': [[9, 3, 4], [4, 0, 16]]}, 'one': {'ts': [[1, 2, 3], [1, 4, 9]]}}
-----------
C> writing
{{{{{{{{{{{{{{}}}}}}}}}}}}}}
S> connection made
S> data received [54]: b'6\x00\x00\x00{"op": "select", "fields": [], "md": {"blarg": 1}}'
S> D> ALL FIELDS
S> list of triggers to run []
S> connection lost
C> status: TSDBStatus.OK
C> payload: {'one': {'blarg': 1, 'order': 1, 'pk': 'one'}}
-----------
C> writing
{{{{{{{{{{{{{{}}}}}}}}}}}}}}
S> connection made
S> data received [68]: b'D\x00\x00\x00{"op": "select", "fields": null, "md": {"order": 1, "blarg": 2}}'
S> D> NO FIELDS
S> list of triggers to run []
S> connection lost
C> status: TSDBStatus.OK
C> payload: {'three': {}}
-----------
C> writing
END (<TSDBStatus.OK: 0>, {'three': {}})
S> connection made
S> data received [77]: b'M\x00\x00\x00{"op": "select", "fields": ["blarg", "mean"], "md": {"blarg": {">=": 2}}}'
S> D> FIELDS ['blarg', 'mean'] ['three', 'four']
S> list of triggers to run []
S> connection lost
C> status: TSDBStatus.OK
C> payload: {'three': {'blarg': 2}, 'four': {'blarg': 2}}
-----------
C> writing
S> connection made
S> data received [88]: b'X\x00\x00\x00{"op": "select", "fields": ["blarg", "std"], "md": {"blarg": {">=": 2}, "order": 1}}'
S> D> FIELDS ['blarg', 'std'] ['three']
S> list of triggers to run []
S> connection lost
C> status: TSDBStatus.OK
C> payload: {'three': {'blarg': 2}}
-----------
C> writing
S> D> ROW {'std': 3.2998316455372216, 'blarg': 1, 'ts': <timeseries.timeseries.TimeSeries object at 0x103aef2e8>, 'mean': 4.666666666666667, 'order': 1, 'pk': 'one'}
S> D> ROW {'order': 2, 'std': 4.9216076867444674, 'mean': 9.6666666666666661, 'ts': <timeseries.timeseries.TimeSeries object at 0x103aef4a8>, 'pk': 'two'}
S> D> ROW {'std': 6.7986926847903799, 'blarg': 2, 'ts': <timeseries.timeseries.TimeSeries object at 0x103aef908>, 'mean': 6.666666666666667, 'order': 1, 'pk': 'three'}
S> D> ROW {'std': 1.699673171197595, 'blarg': 2, 'ts': <timeseries.timeseries.TimeSeries object at 0x103aef860>, 'mean': 1.6666666666666667, 'order': 2, 'pk': 'four'}
```
