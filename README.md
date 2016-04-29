
TimeSeries Utility (CS 207 Project)
========
[![Build Status](https://travis-ci.org/CS207Project/cs207project.svg?branch=master)](https://travis-ci.org/CS207Project/cs207project)
[![Coverage Status](https://coveralls.io/repos/github/CS207Project/cs207project/badge.svg?branch=master)](https://coveralls.io/github/CS207Project/cs207project?branch=master)

Timeseries Database (group project for CS207 Spring 2016)

Description
-----------

Usage
-----

### 1. Setup

- Start the Database Server: `python drivers/go_server.py`

- Start the Web Server: `python drivers/go_webserver.py`

### 2. API Quick Guide

#### SELECT
Select from the timeseries database.

- Endpoint: **/select**
- Verb: **GET**
- Format: json text as a parameter with the key 'query'- i.e url ends with ?query=json_text
- Example:


    payload = {'where':{'order': {'>='1}},
        'fields':['order','vp'],
        'additional':{'sort_by':'-order',
        'limit':10}}

    requests.get(server_url+'/select',
        params={'query':json.dumps(payload)}).content

#### AUGMENTED SELECT
- Endpoint: **/augselect**
- Verb: **GET**
- Format: json text as a parameter with the key 'query'- i.e url ends with ?query=json_text
- Example:


    _, queryts = tsmaker(0.5, 0.2, 0.1)
    payload = {'proc':'corr',
        'target':'d',
        'arg':queryts.to_json(),
        'where': {'pk': v}}

    requests.get(server_url+'/augselect',
        params={'query':json.dumps(payload)}).content

#### INSERT TIMESERIES
- Endpoint: **/tsdb/add/ts**
- Verb: **POST**
- Example:


    def make_insert_ts(primary_key,t):
        return json.dumps({'primary_key':primary_key,
            'ts':t.to_json()})

    meta1,ts1 = tsmaker(0.1,0.2,0.3)
    requests.post(server_url+'/add/ts',
                  make_insert_ts('ts-1', ts1))


#### UPSERT METADATA
- Endpoint: **/tsdb/add/metadata**
- Verb: **POST**
- Example:


    def make_upsert_meta(primary_key, metadata_dict):
        return json.dumps({'primary_key':primary_key,
            'metadata_dict': metadata_dict})

    meta1,ts1 = tsmaker(0.1,0.2,0.3)
    requests.post(server_url+'/add/metadata',
        make_upsert_meta('ts-1', meta1))

#### INSERT TRIGGER
- Endpoint: **/tsdb/add/trigger**
- Verb: **POST**
- Example:


    def make_add_trigger(proc, onwhat, target, arg):
        if hasattr(arg,'to_json'):
            arg = arg.to_json()
        return json.dumps({'proc':proc,
            'onwhat':onwhat,
            'target':target,
            'arg':arg})

    _, queryts = tsmaker(0.5, 0.2, 0.1)
    requests.post(server_url+'/add/trigger',
        make_add_trigger('corr', 'insert_ts', 'd', queryts))

#### REMOVE TRIGGER

- Endpoint: /tsdb/remove/trigger
- Verb: POST


Modules
-------

### timeseries


### tsdb


### procs


### pype


Note
-----

This project has been set up using PyScaffold 2.5.5. For details and usage
information on PyScaffold see [http://pyscaffold.readthedocs.org/](http://pyscaffold.readthedocs.org/)
