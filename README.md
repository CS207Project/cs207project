
Timeseries Database
====================
Group project for CS207 Spring 2016. Team Name: **cs207project**

[![Build Status](https://travis-ci.org/CS207Project/cs207project.svg?branch=master)](https://travis-ci.org/CS207Project/cs207project)
[![Coverage Status](https://coveralls.io/repos/github/CS207Project/cs207project/badge.svg?branch=master)](https://coveralls.io/github/CS207Project/cs207project?branch=master)

### [Documentation](http://cs207project.github.io/cs207project/)


### [Demo](https://github.com/CS207Project/cs207project/blob/master/tests/web_server_testing.ipynb)


### [Live Server](http://www.adjch.me:8080/tsdb)


### Implementation Details

#### 1. Architechure of Persistance
The Persistence of our database system is achieved as follows:
1. The meta data for each time series is stored in a heap file (metaheap). The meta data stores all submitted data, in addition to pointers to the associated time series data in a timeseries heap file.
2. The timeseries heap file (tsheap) stores the actual values of the time series.
3. A Primary Key Index stores the association between primary keys and their associated meta data offset (in metaheap). This index is implemented as a python dictionary in memory, stored using pickle and a write-ahead log.
4. Our database system supports two other types of indices.
    - The TreeIndex is a balanced binary search tree, which supports logarithmic lookup time. This index supports ordered selects, in addition to the standard selection criteria. It is implemented using the bintrees python module. The tree is not currently optimal, and supports O(n) insertion rather than O(log n).
    - The BitMask index is created for low-cardinality meta-data. It does not support ordering on selection.
5. In summary, our database supports O(1) insertion of new timeseries and lookup under primary key, O(log n) read/ select, including various criteria and operators, and O(n) insertion/ updating of metadata, where n is the number of timeseries in the database.

#### 2. Extension beyond milestone2 -- Vantage Point Trees

We implement Vantage Point Trees as descibed in [this paper](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.43.7492). Essentaillly we store a tree strucure in memory that enables us to cut down the number of distance calculations needed to find similar timeseries to `log n` where n is the number of vantage points. This improves performance by an order of magnitude.

#### 3. REST API and Demo
Please see the Demo and Documentation links above.

#### 4. Installation

Clone the repo and follow the instructions in the `.travis.yml` file.
