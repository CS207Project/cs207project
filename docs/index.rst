.. cs207project documentation master file, created by
   sphinx-quickstart on Fri Apr 29 16:48:18 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==================
TimeSeries Utility
==================
(team CS207Project)

.. toctree::
   :maxdepth: 2

   authors
   changes
   license
   api/modules

-----------
Description
-----------

We implement a database that can store time series data and perform fast similarly serach on it.

-----
Usage
-----

1. Setup
========
- Start the Database Server:
::

    python go_server.py

- Start the Web Server:
::

    python go_webserver.py

2. API Quick Guide
==================
i. SELECT
---------
Select from the timeseries database.

- Endpoint: **/select**
- Verb: **GET**
- Format: json text as a parameter with the key 'query'- i.e url ends with `?query=json_text`
- Example:

::

    payload = {'where':{'order': {'>=' : 1}},
        'fields':['order','vp'],
        'additional':{'sort_by':'-order',
        'limit':10}}

    requests.get(server_url+'/select',
        params={'query':json.dumps(payload)}).content

ii. AUGMENTED SELECT
--------------------
Select a set of rows and then run a predefined stored procedure on it

- Endpoint: **/augselect**
- Verb: **GET**
- Format: json text as a parameter with the key 'query'- i.e url ends with `?query=json_text`
- Example:

::

    m, queryts = tsmaker(0.5, 0.2, 0.1)
    payload = {'proc':'corr', 'target':'d', 'arg':queryts.to_json(), 'where': {'pk': v}}
    requests.get(server_url+'/augselect', params={'query':json.dumps(payload)}).content

iii. INSERT TIMESERIES
----------------------
Insert a new timeseries into the database

- Endpoint: **/tsdb/add/ts**
- Verb: **POST**
- Example:

::

    def make_insert_ts(primary_key,t):
        return json.dumps({'primary_key':primary_key,'ts':t.to_json()})

    meta1,ts1 = tsmaker(0.1,0.2,0.3)
    requests.post(server_url+'/add/ts', make_insert_ts('ts-1', ts1))


iv. UPSERT METADATA
-------------------
Update or Insert metadata for a particular timeseries into the database

- Endpoint: **/tsdb/add/metadata**
- Verb: **POST**
- Example:

::

    def make_upsert_meta(primary_key, metadata_dict):
        return json.dumps({'primary_key':primary_key, 'metadata_dict': metadata_dict})

    meta1,ts1 = tsmaker(0.1,0.2,0.3)
    requests.post(server_url+'/add/metadata', make_upsert_meta('ts-1', meta1))

v. INSERT TRIGGER
-----------------
Setup a predefined stored procedure to be run when a particular event occurs in the database.
This is called a trigger.

- Endpoint: **/tsdb/add/trigger**
- Verb: **POST**
- Example:

::

    def make_add_trigger(proc, onwhat, target, arg):
        if hasattr(arg,'to_json'):
            arg = arg.to_json()
        return json.dumps({'proc':proc,'onwhat':onwhat,'target':target,'arg':arg})

    m, queryts = tsmaker(0.5, 0.2, 0.1)
    requests.post(server_url+'/add/trigger', make_add_trigger('corr', 'insert_ts', 'd', queryts))

vi. REMOVE TRIGGER
------------------
Remove a trigger from the database.

- Endpoint: **/tsdb/remove/trigger**
- Verb: **POST**

----
Note
----

This project has been set up using PyScaffold 2.5.5. For details and usage
information on PyScaffold see http://pyscaffold.readthedocs.org/.

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`