"""Defines the types of errors the database server / client / backend can encounter
"""
import enum


class TSDBStatus(enum.IntEnum):
    """
    Class to report the status of the timeseries database after processing
    a request from the client. There are four possible statuses returned.

    0: Everything is okay.
    1: An unknown error has occurred.
    2: The client has attempted an invalid operation.
    3: The request was for an invalid key, most likely a duplicate primary key.
    """
    OK = 0
    UNKNOWN_ERROR = 1
    INVALID_OPERATION = 2
    INVALID_KEY = 3

    @staticmethod
    def encoded_length():
        return 3

    def encode(self):
        return str.encode('{:3d}'.format(self.value))

    @classmethod
    def from_bytes(cls, data):
        return cls(int(data.decode()))
