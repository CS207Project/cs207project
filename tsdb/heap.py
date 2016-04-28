# from .persistantdb import TYPES, TYPE_DEFAULT
import os
import struct
import timeseries
import json

# see https://docs.python.org/3.4/library/struct.html#struct-format-strings
TYPES = {
    'float': 'd',
    'bool': '?',
    'int': 'i'
}

TYPE_DEFAULT = {
    'float': 0.0,
    'bool': False,
    'int': 0
}

TS_FIELD_LENGTH = 4

class HeapFile:
    def __init__(self, heap_file_name):
        self.filename = heap_file_name
        if not os.path.exists(self.filename):
            #DNY: buffering=0 only allowed in binary mode, see python docs
            self.fd = open(self.filename, "xb+", buffering=0)
        else:
            self.fd = open(self.filename, "r+b", buffering=0)
        self.readptr = self.fd.tell()
        self.fd.seek(0,2)#DNY: seek the end of the file
        self.writeptr = self.fd.tell()

class MetaHeapFile(HeapFile):
    def create_compression_string(self, schema):
        fieldList = sorted(list(schema.keys()))
        # pk and ts will be stored in the index file and tsheap file respectively
        fieldList.remove('ts')
        fieldList.remove('pk')
        self.compression_string = ''
        # DNY: ordered list of storage of fields
        self.fields = []
        # DNY: to store default values of each field, as placeholders
        self.fieldsDefaultValues = []
        for field in fieldList:
            self.compression_string += TYPES[schema[field]['type']]
            self.fields.append(field)
            self.fieldsDefaultValues.append(TYPE_DEFAULT[schema[field]['type']])
            # create field to check whether field is set, later
            if schema[field]['type'] != "bool":
                self.compression_string += TYPES['bool']
                self.fields.append(field+"_set")
                self.fieldsDefaultValues.append(False)
        self.byteArrayLength = len(struct.pack(self.compression_string,
                                               *self.fieldsDefaultValues))

    def check_byteArray(self,byteArray):
        "method to double check compression succeeded"
        assert(len(byteArray) == self.byteArrayLength)

    def encode_and_write_meta(self, meta, pk_offset=None):
        "takes metadata and writes to file, return the offset of the write"
        byteArray = struct.pack(self.compression_string,*meta)
        self.check_byteArray(byteArray)
        if pk_offset is None:
            pk_offset = self.writeptr
        self.fd.seek(pk_offset)
        self.fd.write(byteArray)
        # DNY: seek the end of the file in case new element written
        self.fd.seek(0,2)
        self.writeptr = self.fd.tell()
        return pk_offset

    def read_and_return_meta(self,pk_offset):
        self.fd.seek(pk_offset)
        buff = self.fd.read(self.byteArrayLength)
        #check that reading and writing worked
        # print(self.metaFields)
        # print(struct.unpack(self.compression_string,buff))
        return list(struct.unpack(self.compression_string,buff))

class TSHeapFile(HeapFile):
    def encode_and_write_ts(self, ts):
        dataBytes = json.dumps(ts.to_json()).encode()
        lengthFieldBytes = (len(dataBytes)+TS_FIELD_LENGTH).to_bytes(TS_FIELD_LENGTH, byteorder='little')
        byteArray = lengthFieldBytes + dataBytes

        self.fd.seek(self.writeptr)
        ts_offset = self.fd.tell()
        self.fd.write(byteArray)
        self.fd.seek(0,2)#DNY: seek the end of the file
        self.writeptr = self.fd.tell()
        return ts_offset

    def read_and_decode_ts(self, offset):
        self.fd.seek(offset)
        ts_length = int.from_bytes(self.fd.read(TS_FIELD_LENGTH), byteorder='little')
        self.fd.seek(offset + TS_FIELD_LENGTH)
        buff = self.fd.read(ts_length)
        return timeseries.TimeSeries.from_json(json.loads(buff.decode()))