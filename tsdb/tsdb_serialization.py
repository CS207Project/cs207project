import json

LENGTH_FIELD_LENGTH = 4


def serialize(json_obj):#DNY: this is called in the tsdb_server.py (and soon tsdb_client.py) to send bytes
    '''Turn a JSON object into bytes suitable for writing out to the network.

    Includes a fixed-width length field to simplify reconstruction on the other
    end of the wire.'''
    #DNY written
    # encode the JSON string as bytes
    # try:
    json_str = json.dumps(json_obj)
    # except TypeError:
    #     print(json_obj)
    # figure out length, add LFL, and write length wiht size LFL using int.to_bytes() method
    dataBytes = json_str.encode()
    lengthFieldBytes = (len(dataBytes)+LENGTH_FIELD_LENGTH).to_bytes(LENGTH_FIELD_LENGTH, byteorder='little')
    # join the two and returns the bytes on the wire
    return lengthFieldBytes + dataBytes


class Deserializer(object):
    '''A buffering and bytes-to-json engine.

    Data can be received in arbitrary chunks of bytes, and we need a way to
    reconstruct variable-length JSON objects from that interface. This class
    buffers up bytes until it can detect that it has a full JSON object (via
    a length field pulled off the wire). To use this, shove bytes in with the
    append() function and call ready() to check if we've reconstructed a JSON
    object. If True, then call deserialize to return it. That object will be
    removed from this buffer after it is returned.'''

    def __init__(self):
        self.buf = b''
        self.buflen = -1

    def append(self, data):
        self.buf += data
        self._maybe_set_length()

    def _maybe_set_length(self):
        if self.buflen < 0 and len(self.buf) >= LENGTH_FIELD_LENGTH:
            self.buflen = int.from_bytes(self.buf[0:LENGTH_FIELD_LENGTH], byteorder="little")

    def ready(self):
        return (self.buflen > 0 and len(self.buf) >= self.buflen)

    def deserialize(self):#DNY: only called once self.ready() returns true (see tsdb_server.py)
        json_str = self.buf[LENGTH_FIELD_LENGTH:self.buflen].decode()#DNY: defaults to utf-8 encoding (see docs)
        self.buf = self.buf[self.buflen:]
        self.buflen = -1
        self._maybe_set_length() # There may be more data in the buffer already, so preserve it
        try:
            obj = json.loads(json_str)
            return obj
        except json.JSONDecodeError:
            print('Invalid JSON object received:\n'+str(json_str))
            return None
