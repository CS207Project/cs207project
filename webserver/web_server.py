"""Implementation of an async WebServer with RESTful api that talks to the TimeSeries Database.

"""

import asyncio
from aiohttp import web
from tsdb import TSDBClient
from tsdb import TSDBStatus
import timeseries as ts
import json

class Handlers:
    """These are the event handlers for the various endpoints defined in our rest API
    """
    def __init__(self):
        self.client = TSDBClient()

    async def homepage_handler(self,request):
        """Handler for Homepage

        Parameters
        ----------
        request : aiotttp.request
            request object with details of the request that was sent to the server

        Returns
        -------
        web.Response
            Text showing the various endpoints that are available
        """
        body_txt = """
        Time Series Database

        https://github.com/CS207Project/cs207project

        """
        return web.Response(body=body_txt.encode('utf-8'))

    async def select_handler(self,request):
        """Handler for Select

        Parameters
        ----------
        request : aiotttp.request
            request object with details of the request that was sent to the server

            request.GET['query'] should exist or an error is returned **REQUIRED**

            request.GET['query']['fields'] -> json encoded list of fields to be selected.
            Default is just the primary_key

            request.GET['query']['where'] -> json encoded metadata_dict describing the select criteria.
            Default will return all rows in the database

            request.GET['query']['additional'] -> json encoded additional information for the select.
            Default ignore the additional info.

        Returns
        -------
        web.Response
            JSON encoded results of the select
        """
        try:
            if 'query' not in request.GET:
                raise ValueError("'query' must be sent with a select",request.GET)

            json_query = json.loads(request.GET['query'])

            fields = json_query['fields'] if 'fields' in json_query else None
            metadata_dict = json_query['where'] if 'where' in json_query else {}
            additional = json_query['additional'] if 'additional' in json_query else None
            status,payload = await self.client.select(metadata_dict,fields,additional)

        except Exception as error:
            payload = {"msg": "Could not parse request. Please see documentation."}
            payload["type"] = str(type(error))
            payload["args"] = str(error.args)

        finally:
            return web.Response(body=json.dumps(payload).encode('utf-8'))

    async def make_vp_tree_handler(self,request):
        """Handler for Make VP Tree

        Parameters
        ----------
        request : aiotttp.request
            request object with details of the request that was sent to the server

            request.GET['query'] should exist or an error is returned **REQUIRED**

        Returns
        -------
        web.Response
            JSON encoded results of the select
        """
        try:
            if 'query' not in request.GET:
                raise ValueError("'query' must be sent with a select",request.GET)

            json_query = json.loads(request.GET['query'])
            status,payload = await self.client.make_vp_tree()

            if status ==TSDBStatus.OK:
                textResp = "WriteSuccessful"
            else:
                raise Exception("Write Failed")

        except Exception as error:
            textResp = {"msg": "Could not parse request. Please see documentation."}
            textResp["type"] = str(type(error))
            textResp["args"] = str(error.args)

        finally:
            return web.Response(body=json.dumps(textResp).encode('utf-8'))

    async def augselect_handler(self,request):
        """Handler for Augmented Select

        Parameters
        ----------
        request : aiotttp.request
            request object with details of the request that was sent to the server

            request.json()['proc'] -> the stored proc that will be called. **REQUIRED**

            request.json()['target'] -> json encoded list of what the output of the stored proc
            will be called. **REQUIRED**

            request.json()['where'] -> json encoded metadata_dict describing the select criteria.
            Default will return all rows in the database

            request.json()['additional'] -> json encoded additional information for the select.
            Default ignores the additional info.

            request.json()['arg'] -> json encoded additional argument sent to the stored proc.
            Default ignores the arg

        Returns
        -------
        web.Response
            JSON encoded results of the augmented select
        """
        try:
            json_query = await request.json()
            target = json_query['target']
            proc = json_query['proc']

            metadata_dict = json_query['where'] if 'where' in json_query else {}
            additional = json_query['additional'] if 'additional' in json_query else None
            arg = json_query['arg'] if 'arg' in json_query else None

            status,payload = await self.client.augmented_select(proc,target,arg
                                                                ,metadata_dict
                                                                ,additional)
        except Exception as error:
            payload = {"msg": "Could not parse request. Please see documentation."}
            payload["type"] = str(type(error))
            payload["args"] = str(error.args)

        finally:
            return web.Response(body=json.dumps(payload).encode('utf-8'))

    async def find_similar_handler(self,request):
        """Handler for Find Similar

        Parameters
        ----------
        request : aiotttp.request
            request object with details of the request that was sent to the server

            request.json()['arg'] -> json encoded timeseries that is the reference to
            which we're trying to find the closest match **REQUIRED**

            request.json()['vpkeys'] -> list of vantage point trees that correspond
            to [d_vp-1, d_vp-2, ...] in the correct order **REQUIRED**

        Returns
        -------
        web.Response
            JSON encoded results of the augmented select
        """
        try:
            json_query = await request.json()
            arg = json_query['arg']

            status,payload = await self.client.find_similar(arg)
        except Exception as error:
            payload = {"msg": "Could not parse request. Please see documentation."}
            payload["type"] = str(type(error))
            payload["args"] = str(error.args)

        finally:
            return web.Response(body=json.dumps(payload).encode('utf-8'))


    async def add_ts_handler(self,request):
        """Handler for add time series

        Parameters
        ----------
        request : aiotttp.request
            request object with details of the request that was sent to the server

            request must be JSON encoded

            request.json()['primary_key'] --> primary key for this timeseries in the database. **REQUIRED**

            request.json()['ts'] --> timeseries to be added. **REQUIRED**


        Returns
        -------
        web.Response
            JSON encoded text indicating success or failure of write
        """
        try:
            req_dict = await request.json()

            pk = req_dict['primary_key']
            t = ts.TimeSeries(*req_dict['ts'])
            status, payload = await self.client.insert_ts(pk,t)

            if status ==TSDBStatus.OK:
                textResp = "WriteSuccessful"
            else:
                raise Exception("Write Failed")

        except Exception as error:
            textResp = {"msg": "Could not parse request. Please see documentation."}
            textResp["type"] = str(type(error))
            textResp["args"] = str(error.args)

        finally:
            return web.Response(body=json.dumps(textResp).encode('utf-8'))

    async def delete_ts_handler(self,request):
        """Handler for delete time series

        Parameters
        ----------
        request : aiotttp.request
            request object with details of the request that was sent to the server

            request must be JSON encoded

            request.json()['primary_key'] --> primary key for this timeseries in the database. **REQUIRED**


        Returns
        -------
        web.Response
            JSON encoded text indicating success or failure of write
        """
        try:
            req_dict = await request.json()

            pk = req_dict['primary_key']
            status, payload = await self.client.delete_ts(pk)

            if status ==TSDBStatus.OK:
                textResp = "WriteSuccessful"
            else:
                raise Exception("Write Failed")

        except Exception as error:
            textResp = {"msg": "Could not parse request. Please see documentation."}
            textResp["type"] = str(type(error))
            textResp["args"] = str(error.args)

        finally:
            return web.Response(body=json.dumps(textResp).encode('utf-8'))

    async def add_trigger_handler(self,request):
        """Handler for add trigger

        Parameters
        ----------
        request : aiotttp.request
            request object with details of the request that was sent to the server

            request must be JSON encoded

            request.json()['proc'] --> name of the predefined stored proc to be run **REQUIRED**

            request.json()['onwhat'] --> name of the event after which trigger is run **REQUIRED**

            request.json()['target'] --> list of names of the output varibles in which we store the result of the stored procedure **REQUIRED**

            request.json()['arg'] --> optinal argument sent to the stored procedure

        Returns
        -------
        web.Response
            JSON encoded text indicating success or failure of write
        """
        try:
            req_dict = await request.json()
            print(req_dict)
            status, payload = await self.client.add_trigger(
                    req_dict['proc'],req_dict['onwhat'],req_dict['target'], req_dict['arg'])
            if status ==TSDBStatus.OK:
                textResp = "WriteSuccessful"
            else:
                raise Exception("Write Failed")

        except Exception as error:
            textResp = {"msg": "Could not parse request. Please see documentation."}
            textResp["type"] = str(type(error))
            textResp["args"] = str(error.args)

        finally:
            return web.Response(body=json.dumps(textResp).encode('utf-8'))

    async def remove_trigger_handler(self,request):
        """Handler for remove trigger

        Parameters
        ----------
        request : aiotttp.request
            request object with details of the request that was sent to the server

            request must be JSON encoded

            request.json()['proc'] --> name of the predefined stored proc to be run **REQUIRED**

            request.json()['onwhat'] --> name of the event after which trigger is run **REQUIRED**

        Returns
        -------
        web.Response
            JSON encoded text indicating success or failure of write
        """
        try:
            req_dict = await request.json()
            print(req_dict)
            status, payload = await self.client.remove_trigger(
                    req_dict['proc'],req_dict['onwhat'])
            if status ==TSDBStatus.OK:
                textResp = "WriteSuccessful"
            else:
                raise Exception("Write Failed")

        except Exception as error:
            textResp = {"msg": "Could not parse request. Please see documentation."}
            textResp["type"] = str(type(error))
            textResp["args"] = str(error.args)

        finally:
            return web.Response(body=json.dumps(textResp).encode('utf-8'))

    async def add_metadata_handler(self,request):
        """Handler for remove trigger

        Parameters
        ----------
        request : aiotttp.request
            request object with details of the request that was sent to the server

            request must be JSON encoded

            request.json()['primary_key'] --> primary key for this timeseries in the database. **REQUIRED**

            request.json()['metadata_dict'] --> dictionary containing the metadata that we want to add to this timeseries **REQUIRED**

        Returns
        -------
        web.Response
            JSON encoded text indicating success or failure of write
        """
        try:
            req_dict = await request.json()
            status, payload = await self.client.upsert_meta(
                    req_dict['primary_key'],req_dict['metadata_dict'])
            if status ==TSDBStatus.OK:
                textResp = "WriteSuccessful"
            else:
                raise Exception("Write Failed")

        except Exception as error:
            textResp = {"msg": "Could not parse request. Please see documentation."}
            textResp["type"] = str(type(error))
            textResp["args"] = str(error.args)

        finally:
            return web.Response(body=json.dumps(textResp).encode('utf-8'))

class WebServer:
    """Implements a webserver with some endpoints for REST api calls

    Attributes
    ----------
    handler : Handlers
        the hnadlers for the endpoints that we define the server
    app : web.Application
        aiotttp web application that handles the server
    """
    def __init__(self):
        "set up the server with some endpoints"
        self.handler = Handlers()
        self.app = web.Application()
        self.app.router.add_route('GET', '/tsdb', self.handler.homepage_handler)
        self.app.router.add_route('GET', '/tsdb/select',self.handler.select_handler)
        self.app.router.add_route('GET', '/tsdb/add/vptree',self.handler.make_vp_tree_handler)
        self.app.router.add_route('POST', '/tsdb/augselect',self.handler.augselect_handler)
        self.app.router.add_route('POST', '/tsdb/find_similar', self.handler.find_similar_handler)
        self.app.router.add_route('POST', '/tsdb/add/ts', self.handler.add_ts_handler)
        self.app.router.add_route('POST', '/tsdb/add/trigger', self.handler.add_trigger_handler)
        self.app.router.add_route('POST', '/tsdb/delete/trigger', self.handler.remove_trigger_handler)
        self.app.router.add_route('POST', '/tsdb/add/metadata', self.handler.add_metadata_handler)
        self.app.router.add_route('POST', '/tsdb/delete/ts', self.handler.delete_ts_handler)

    def run(self):
        "run the webserver"
        web.run_app(self.app)
