```
(py35)➜  cs207project git:(simplest) sh both.sh
Generating LALR tables
S> Starting TSDB server on port 9999
Generating LALR tables
S> data received [66]: b'B\x00\x00\x00{"ts": [[1, 2, 3], [1, 4, 9]], "pk": "one", "op": "insert_ts"}'
S> connection lost
C> status: TSDBStatus.OK
C> payload: None
-----------
C> writing
S> data received [67]: b'C\x00\x00\x00{"ts": [[2, 3, 4], [4, 9, 16]], "pk": "two", "op": "insert_ts"}'
S> connection lost
C> status: TSDBStatus.OK
C> payload: None
-----------
C> writing
S> data received [69]: b'E\x00\x00\x00{"ts": [[9, 3, 4], [4, 0, 16]], "pk": "three", "op": "insert_ts"}'
S> connection lost
C> status: TSDBStatus.OK
C> payload: None
-----------
C> writing
S> data received [67]: b'C\x00\x00\x00{"ts": [[0, 0, 4], [1, 0, 4]], "pk": "four", "op": "insert_ts"}'
S> connection lost
C> status: TSDBStatus.OK
C> payload: None
-----------
C> writing
S> data received [70]: b'F\x00\x00\x00{"pk": "one", "op": "upsert_meta", "md": {"order": 1, "blarg": 1}}'
S> connection lost
C> status: TSDBStatus.OK
C> payload: None
-----------
C> writing
S> data received [58]: b':\x00\x00\x00{"pk": "two", "op": "upsert_meta", "md": {"order": 2}}'
S> connection lost
C> status: TSDBStatus.OK
C> payload: None
-----------
C> writing
S> data received [72]: b'H\x00\x00\x00{"pk": "three", "op": "upsert_meta", "md": {"order": 1, "blarg": 2}}'
S> connection lost
C> status: TSDBStatus.OK
C> payload: None
-----------
C> writing
S> data received [71]: b'G\x00\x00\x00{"pk": "four", "op": "upsert_meta", "md": {"order": 2, "blarg": 2}}'
S> connection lost
C> status: TSDBStatus.OK
C> payload: None
-----------
C> writing
S> data received [30]: b'\x1e\x00\x00\x00{"op": "select", "md": {}}'
S> connection lost
C> status: TSDBStatus.OK
C> payload: ['two', 'four', 'three', 'one']
-----------
C> writing
S> data received [40]: b'(\x00\x00\x00{"op": "select", "md": {"order": 1}}'
S> connection lost
C> status: TSDBStatus.OK
C> payload: ['three', 'one']
-----------
C> writing
S> data received [40]: b'(\x00\x00\x00{"op": "select", "md": {"blarg": 1}}'
S> connection lost
C> status: TSDBStatus.OK
C> payload: ['one']
-----------
C> writing
S> data received [52]: b'4\x00\x00\x00{"op": "select", "md": {"order": 1, "blarg": 2}}'
S> connection lost
C> status: TSDBStatus.OK
C> payload: ['three']
-----------
C> writing
END (<TSDBStatus.OK: 0>, ['three'])
```
