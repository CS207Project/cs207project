"""Base Classes that define the interfaces implemented elsewhere

"""
import abc

class BaseIndex(metaclass = abc.ABCMeta):
    """Interface that all indices should support
    """
    @abc.abstractmethod
    def insert(self, fieldValue, pk):
        """insert the value into the appropriate place in the tree
        """
        pass

    @abc.abstractmethod
    def remove(self, fieldValue, pk):
        """remove a primary key from the index"""
        pass

    @abc.abstractmethod
    def getEqual(self, fieldValue):
        """return set of primary keys that match this fieldValue"""
        pass

class BaseDB(metaclass = abc.ABCMeta):
    """Interface that all Databases should support
    """

    @abc.abstractmethod
    def __getitem__(self,key):
        """Dunder method to get the the values at a given primary_key"""
        pass

    @abc.abstractmethod
    def insert_ts(self, pk, ts):
        "Given a pk and a timeseries, insert them"
        pass

    @abc.abstractmethod
    def delete_ts(self, pk):
        "Given a pk, remove that timeseries from the database"
        pass

    @abc.abstractmethod
    def upsert_meta(self, pk, meta):
        """Given a primary key and a dict of meta fields, value pairs, upsert
        them as long as they're in the schema.
        """
        pass

    @abc.abstractmethod
    def select(self, meta, fields_to_ret, additional):
        """Select from the database
        """
        pass
