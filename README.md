
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


#### 2. Extension beyond milestone2 -- Vantage Point Trees

We implement Vantage Point Trees as descibed in [this paper](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.43.7492). Essentaillly we store a tree strucure in memory that enables us to cut down the number of distance calculations needed to find similar timeseries to `log n` where n is the number of vantage points. This improves performance by an order of magnitude.

#### 3. REST API and Demo
Please see the Demo and Documentation links above.

#### 4. Installation

Clone the repo and follow the instructions in the `.travis.yml` file.
