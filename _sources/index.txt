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

    python go_server.py -len 1024 -vps 10 &

- Start the Web Server:
::

    python go_webserver.py &

2. API Quick Guide
==================

We recommned using our WebClient to talk to the database. It
implements the REST calls that are supported and returns a
`requests.response` object. See the demo_ for a full example.

.. _demo: https://github.com/CS207Project/cs207project/blob/master/tests/web_server_testing.ipynb


::

    w = WebClient('http://localhost:8080')
    # or
    w = WebClient('http://www.adjch.me:8080')

i. SELECT
---------
Select from the timeseries database.

- Endpoint: **/select**
- Verb: **GET**
- Format: json text as a parameter with the key 'query'- i.e url ends with `?query=json_text`
- Example:

::

    r = w.select()
    assert r.status_code == 200
    # or
    r = w.select(additional={'sort_by':'+pk','limit':100})
    assert r.status_code == 200

ii. AUGMENTED SELECT
--------------------
Select a set of rows and then run a predefined stored procedure on it

- Endpoint: **/augselect**
- Verb: **POST**
- Example:

::

    r = w.augselect('corr','d',where_dict,arg=query)


iii. INSERT TIMESERIES
----------------------
Insert a new timeseries into the database

- Endpoint: **/tsdb/add/ts**
- Verb: **POST**
- Example:

::

    r = w.insert_ts(primary_key, timeseries)
    assert r.status_code == 200


iv. UPSERT METADATA
-------------------
Update or Insert metadata for a particular timeseries into the database

- Endpoint: **/tsdb/add/metadata**
- Verb: **POST**
- Example:

::

    r = w.upsert_meta(primary_key, metadict)

v. INSERT TRIGGER
-----------------
Setup a predefined stored procedure to be run when a particular event occurs in the database.
This is called a trigger.

- Endpoint: **/tsdb/add/trigger**
- Verb: **POST**
- Example:

::

    r = w.add_trigger('junk', 'insert_ts', None, 'db:one:ts')
    assert r.status_code == 200

vi. REMOVE TRIGGER
------------------
Remove a trigger from the database.

- Endpoint: **/tsdb/remove/trigger**
- Verb: **POST**
- Example:

::

    r = w.remove_trigger('junk', 'insert_ts')


vii. FIND SIMILAR
------------------
Find the timeseries in our database that is most similar to the query. If a
vantage point tree has been made it will be used. If not regular vantage points
will be used.

- Endpoint: **/tsdb/find_similar**
- Verb: **POST**
- Example:

::

    r = w.find_similar(query)


vii. MAKE VP TREE
------------------
Make a vantage point tree with the current state of the database.

- Endpoint: **/tsdb/add/vptree**
- Verb: **GET**
- Example:

::

    r = w.make_vp_tree()

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
