"""Utilites to interact with the webserver. Supports the endpoints that are
exposed to the user via the requests module.

"""

import requests
import timeseries as ts
import numpy as np
import requests
import json

class WebClient:
    """Talks to the websever
    """

    def __init__(self,server_url):
        self.server_url = server_url
        self.endpoints = {
            'homepage' : ['GET', '/tsdb'],
            'select': ['GET', '/tsdb/select'],
            'augselect' : ['POST', '/tsdb/augselect'],
            'find_similar' : ['POST', '/tsdb/find_similar'],
            'insert_ts' : ['POST', '/tsdb/add/ts'],
            'add_trigger' : ['POST', '/tsdb/add/trigger'],
            'remove_trigger' : ['POST', '/tsdb/delete/trigger'],
            'upsert_meta' : ['POST', '/tsdb/add/metadata'],
            'delete_ts' : ['POST', '/tsdb/delete/ts'],
            'make_vp_tree' : ['GET', '/tsdb/add/vptree'],
        }
    def _dispatch_request(self, verb, endpoint, arg):
        if verb == 'GET':
            return requests.get(self.server_url+endpoint,
                            params={'query':arg})
        elif verb == 'POST':
            return requests.post(self.server_url+endpoint,arg)
        else:
            raise ValueError("Non GET / POST verbs not allowed")

    def insert_ts(self, primary_key,t):
        json_query = json.dumps({'primary_key':primary_key, 'ts':t.to_json()})
        verb, endpoint = self.endpoints['insert_ts']
        return self._dispatch_request(verb, endpoint, json_query)

    def upsert_meta(self, primary_key, metadata_dict):
        json_query = json.dumps({'primary_key':primary_key, 'metadata_dict': metadata_dict})
        verb, endpoint = self.endpoints['upsert_meta']
        return self._dispatch_request(verb, endpoint, json_query)

    def add_trigger(self, proc, onwhat, target, arg):
        if hasattr(arg,'to_json'):
            arg = arg.to_json()
        json_query = json.dumps({'proc':proc,'onwhat':onwhat,'target':target,'arg':arg})
        verb, endpoint = self.endpoints['add_trigger']
        return self._dispatch_request(verb, endpoint, json_query)

    def remove_trigger(self, proc, onwhat):
        json_query = json.dumps({'proc':proc,'onwhat':onwhat})
        verb, endpoint = self.endpoints['remove_trigger']
        return self._dispatch_request(verb, endpoint, json_query)

    def delete_ts(self, primary_key):
        json_query = json.dumps({'primary_key':primary_key})
        verb, endpoint = self.endpoints['delete_ts']
        return self._dispatch_request(verb, endpoint, json_query)

    def find_similar(self, arg, vpkeys):
        if hasattr(arg,'to_json'):
            arg = arg.to_json()
        json_query = json.dumps({'arg':arg,'vpkeys': vpkeys})
        verb, endpoint = self.endpoints['find_similar']
        return self._dispatch_request(verb, endpoint, json_query)

    def select(self, where = {}, fields = None, additional = None):
        json_query = json.dumps({'where': where, 'fields': fields,
                                'additional': additional})
        verb, endpoint = self.endpoints['select']
        return self._dispatch_request(verb, endpoint, json_query)

    def make_vp_tree(self):
        json_query = json.dumps({})
        verb, endpoint = self.endpoints['make_vp_tree']
        return self._dispatch_request(verb, endpoint, json_query)

    def augselect(self, proc, target, where = {}, additional = None, arg = None):
        if hasattr(arg,'to_json'):
            arg = arg.to_json()

        json_query = json.dumps({'proc': proc, 'target': target,
                                'where': where, 'additional': additional,
                                'arg': arg})
        verb, endpoint = self.endpoints['augselect']
        return self._dispatch_request(verb, endpoint, json_query)

    def homepage(self):
        json_query = json.dumps({})
        verb, endpoint = self.endpoints['homepage']
        return self._dispatch_request(verb, endpoint, json_query)
