"""Encapluation for all the operations. Communication also passes through here.
"""

import timeseries as ts
from .tsdb_error import *
from collections import OrderedDict
import numbers

# Interface classes for TSDB network operations.
# These are a little clunky (extensibility is meh), but it does provide strong
# typing for TSDB ops and a straightforward mechanism for conversion to/from
# JSON objects.

#DNY: Ops are operations sent to the database, to be run.
# IMPT! they inherit from dict, so they can be indexed!
class TSDBOp(dict):
    def __init__(self, op):
        self['op'] = op

    def to_json(self, obj=None):
        # This is both an interface function and its own helper function.
        # It recursively converts elements in a hierarchical data structure
        # into a JSON-encodable form. It does *not* handle class instances
        # unless they have a 'to_json' method.
        if obj is None:
            obj = self
        json_dict = OrderedDict()
        if isinstance(obj, str) or isinstance(obj,numbers.Number) or not hasattr(obj, '__len__') or obj is None:
            return obj
        if isinstance(obj, list):
            return [self.to_json(o) for o in obj]
        if isinstance(obj, tuple):
            return (self.to_json(o) for o in obj)
        for k, v in obj.items():
            if isinstance(v, str) or isinstance(obj,numbers.Number) or not hasattr(v, '__len__') or v is None:
                json_dict[k] = v
            elif isinstance(v, TSDBStatus):
                json_dict[k] = v.name
            elif isinstance(v, list):
                json_dict[k] = [self.to_json(i) for i in v]
            elif isinstance(v, dict):
                json_dict[k] = self.to_json(v)
            elif hasattr(v, 'to_json'):
                json_dict[k] = v.to_json()
            else:
                raise TypeError('Cannot convert object to JSON: '+str(v))
        return json_dict

    @classmethod
    def from_json(cls, json_dict):
        if 'op' not in json_dict:
            raise TypeError('Not a TSDB Operation: '+str(json_dict))
        if json_dict['op'] not in typemap:
            raise TypeError('Invalid TSDB Operation: '+str(json_dict['op']))
        return typemap[json_dict['op']].from_json(json_dict) #DNY return appropriate type


class TSDBOp_InsertTS(TSDBOp):
    def __init__(self, pk, ts):
        super().__init__('insert_ts')
        self['pk'], self['ts'] = pk, ts

    @classmethod
    def from_json(cls, json_dict):
        # print(json_dict)
        return cls(json_dict['pk'], ts.TimeSeries(*(json_dict['ts'])))
        #DNY: timeseries encoded as list [[t1,t2,...], [v1,v2,...]]

class TSDBOp_DeleteTS(TSDBOp):
    def __init__(self, pk):
        super().__init__('delete_ts')
        self['pk'] = pk

    @classmethod
    def from_json(cls, json_dict):
        return cls(json_dict['pk'])

class TSDBOp_Return(TSDBOp):

    def __init__(self, status, op, payload=None):
        super().__init__(op)
        self['status'], self['payload'] = status, payload

    @classmethod
    def from_json(cls, json_dict):  #should not be used
        return cls(json_dict['status'],json_dict['op'],json_dict['payload'])

class TSDBOp_UpsertMeta(TSDBOp):

    def __init__(self, pk, md):
        #print('-----------')
        super().__init__('upsert_meta')
        self['pk'], self['md'] = pk, md

    @classmethod
    def from_json(cls, json_dict):
        return cls(json_dict['pk'], json_dict['md'])


class TSDBOp_Select(TSDBOp):

    def __init__(self, md, fields, additional):
        super().__init__('select')
        self['md'] = md
        self['fields'] = fields
        self['additional'] = additional

    @classmethod
    def from_json(cls, json_dict):
        return cls(json_dict['md'], json_dict['fields'], json_dict['additional'])

class TSDBOp_AddTrigger(TSDBOp):

    def __init__(self, proc, onwhat, target, arg):
        super().__init__('add_trigger')
        self['proc'] = proc
        self['onwhat'] = onwhat
        self['target'] = target
        self['arg'] = arg

    @classmethod
    def from_json(cls, json_dict):
        return cls(json_dict['proc'], json_dict['onwhat'], json_dict['target'], json_dict['arg'])

class TSDBOp_RemoveTrigger(TSDBOp):

    def __init__(self, proc, onwhat):
        super().__init__('remove_trigger')
        self['proc'] = proc
        self['onwhat'] = onwhat

    @classmethod
    def from_json(cls, json_dict):
        return cls(json_dict['proc'], json_dict['onwhat'])

class TSDBOp_AugmentedSelect(TSDBOp):
    """
    A hybrid of select, and add trigger, we only miss the onwhat key as this op
    is used as an add on to selects. We remove the fields arg from select, as
    the only fields sent back are the ones in target, which is used as in
    add_trigger, except that instead of upserting meta with the targets, that
    data is sent back to the user.
    """
    def __init__(self, proc, target, arg, md, additional):
        super().__init__('augmented_select')
        self['md'] = md
        self['additional'] = additional
        self['proc'] = proc
        self['arg'] = arg
        self['target'] = target

    @classmethod
    def from_json(cls, json_dict):
        return cls(json_dict['proc'], json_dict['target'], json_dict['arg'], json_dict['md'], json_dict['additional'])

class TSDBOp_FindSimilar(TSDBOp):
    """Find the timeseries in the DB closest to this one based on the predefined
    distance metric
    """
    def __init__(self, arg, vpkeys):
        super().__init__('find_similar')
        self['arg'] = arg
        self['vpkeys'] = vpkeys

    @classmethod
    def from_json(cls, json_dict):
        # print("in TSDBOp_FindSimilar: ", type(json_dict))
        arg = json_dict['arg']
        vpkeys = json_dict['vpkeys']
        # print("extracted")
        return cls(json_dict['arg'], json_dict['vpkeys'])

# This simplifies reconstructing TSDBOp instances from network data.
typemap = {
  'insert_ts': TSDBOp_InsertTS,
  'upsert_meta': TSDBOp_UpsertMeta,
  'select': TSDBOp_Select,
  'augmented_select': TSDBOp_AugmentedSelect,
  'add_trigger': TSDBOp_AddTrigger,
  'remove_trigger': TSDBOp_RemoveTrigger,
  'delete_ts': TSDBOp_DeleteTS,
  'find_similar': TSDBOp_FindSimilar
}
