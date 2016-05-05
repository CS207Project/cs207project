#!/usr/bin/env python3
from webserver import WebServer
import timeseries as ts
import subprocess
import time
import unittest
import numpy as np
import requests
import json

identity = lambda x: x
to_int = lambda x:int(x)
to_float = lambda x:float(x)
to_bool = lambda x:bool(x)

schema = {
  'pk': {'convert': identity, 'index': None},  #will be indexed anyways
  'ts': {'convert': identity, 'index': None},
  'order': {'convert': to_int, 'index': 1},
  'blarg': {'convert': to_int, 'index': 1},
  'useless': {'convert': identity, 'index': None},
  'mean': {'convert': to_float, 'index': 1},
  'std': {'convert': to_float, 'index': 1},
  'vp': {'convert': to_bool, 'index': 1}
}

TS_LENGTH = 100
NUMVPS = 5

from scipy.stats import norm

# m is the mean, s is the standard deviation, and j is the jitter
# the meta just fills in values for order and blarg from the schema
def tsmaker(m, s, j):
    "returns metadata and a time series in the shape of a jittered normal"
    meta={}
    meta['order'] = int(np.random.choice([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]))
    meta['blarg'] = int(np.random.choice([1, 2]))
    t = np.arange(0.0, 1.0, 1/TS_LENGTH)
    v = norm.pdf(t, m, s) + j*np.random.randn(TS_LENGTH)
    return meta, ts.TimeSeries(t, v)

def make_insert_ts(primary_key,t):
    return json.dumps({'primary_key':primary_key, 'ts':t.to_json()})

def make_upsert_meta(primary_key, metadata_dict):
    return json.dumps({'primary_key':primary_key, 'metadata_dict': metadata_dict})

def make_add_trigger(proc, onwhat, target, arg):
    if hasattr(arg,'to_json'):
        arg = arg.to_json()
    return json.dumps({'proc':proc,'onwhat':onwhat,'target':target,'arg':arg})

def make_remove_trigger(proc, onwhat):
    return json.dumps({'proc':proc,'onwhat':onwhat})

class WebServerTests(unittest.TestCase):

    def setUp(self):
        # start DB server
        self.server_log_file = open('.tsdb_server.log.testweb','w')
        self.server_proc = subprocess.Popen(['python', 'go_server.py']
                ,stdout=self.server_log_file,stderr=subprocess.STDOUT)
        time.sleep(3)

        # start webserver
        self.server_url = 'http://localhost:8080/tsdb'
        self.webserver_log_file = open('.web_server.log.testweb','w')
        self.webserver_proc = subprocess.Popen(['python', 'go_webserver.py']
                ,stdout=self.webserver_log_file,stderr=subprocess.STDOUT)
        time.sleep(3)

        np.random.seed(12345)
        self.N_ts = 50
        self.N_vp = NUMVPS

        # choose 5 distinct vantage point time series
        self.vpkeys = ["ts-{}".format(i) for i in np.random.choice(range(self.N_ts), size=self.N_vp, replace=False)]

    def tearDown(self):
        self.server_proc.terminate()
        self.server_log_file.close()

        self.webserver_proc.terminate()
        self.webserver_log_file.close()

    def test_addTrigger(self):
        r = requests.post(self.server_url+'/add/trigger',make_add_trigger(
                                'junk', 'insert_ts', None, 'db:one:ts'))
        self.assertEqual(r.status_code, 200)

        r = requests.post(self.server_url+'/add/trigger',make_add_trigger(
                                'stats', 'insert_ts', ['mean', 'std'], None))
        self.assertEqual(r.status_code, 200)

    def test_main(self):

        #Set up 50 time series
        mus = np.random.uniform(low=0.0, high=1.0, size=self.N_ts)
        sigs = np.random.uniform(low=0.05, high=0.4, size=self.N_ts)
        jits = np.random.uniform(low=0.05, high=0.2, size=self.N_ts)

        # dictionaries for time series and their metadata
        tsdict={}
        metadict={}
        for i, m, s, j in zip(range(self.N_ts), mus, sigs, jits):
            meta, tsrs = tsmaker(m, s, j)
            # the primary key format is ts-1, ts-2, etc
            pk = "ts-{}".format(i)
            tsdict[pk] = tsrs
            meta['vp'] = False # augment metadata with a boolean asking if this is a  VP.
            metadict[pk] = meta

        for i in range(self.N_vp):
            # add 5 triggers to upsert distances to these vantage points
            requests.post(self.server_url+'/add/trigger',
                          make_add_trigger('corr', 'insert_ts', ["d_vp-{}".format(i)], tsdict[self.vpkeys[i]]))
            # change the metadata for the vantage points to have meta['vp']=True
            metadict[self.vpkeys[i]]['vp']=True
        # Having set up the triggers, now inser the time series, and upsert the metadata
        for k in tsdict:
            requests.post(self.server_url+'/add/ts',
                          make_insert_ts(k, tsdict[k]))
            requests.post(self.server_url+'/add/metadata',
                          make_upsert_meta(k, metadict[k]))

        #we first create a query time series.
        _, query = tsmaker(0.5, 0.2, 0.1)

        # Step 1: in the vpdist key, get  distances from query to vantage points
        # this is an augmented select
        vpdist = {}
        payload = {'proc':'corr','target':'d','arg':query.to_json()}
        for v in self.vpkeys:
            payload['where'] = {'pk': v}
            r = requests.get(self.server_url+'/augselect',params={'query':json.dumps(payload)})
            results = json.loads(r.content.decode('utf-8'))
            vpdist[v] = results[v]['d']

        closest_vpk = min(self.vpkeys,key=lambda v:vpdist[v])

        # Step 2: find all time series within 2*d(query, nearest_vp_to_query)
        #this is an augmented select to the same proc in correlation
        payload = {'proc':'corr','target':'d','arg':query.to_json()}
        payload['where'] = {'d_'+closest_vpk: {'<=': 2*vpdist[closest_vpk]}}
        r = requests.get(self.server_url+'/augselect',params={'query':json.dumps(payload)})
        results = json.loads(r.content.decode('utf-8'))

        #2b: find the smallest distance amongst this ( or k smallest)
        #you can do this in local code
        nearestwanted = min(results.keys(),key=lambda p: results[p]['d'])
        self.assertEqual(nearestwanted,'ts-0')


if __name__ == '__main__':
    unittest.main()
