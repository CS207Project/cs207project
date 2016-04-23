import asyncio
from aiohttp import web
from tsdb import TSDBClient
from tsdb import TSDBStatus
import timeseries as ts
import json

class Handlers:
    def __init__(self):
        self.client = TSDBClient()
        pass

    async def homepage_handler(self,request):
        body_txt = """
        RESTful API Implementation:

        /tsdb --> homepage
        /tsdb/select --> select
        /tsdb/augselect --> augmented select
        /tsdb/add/ts --> insert timeseries
        /tsdb/add/trigger --> add trigger
        /tsdb/remove/trigger --> remove trigger
        /tsdb/add/metadata --> insert metadata

        """
        return web.Response(body=body_txt.encode('utf-8'))

    async def select_handler(self,request):
        if 'query' not in request.GET:
            return web.Response(body=json.dumps(
                                "'query' must be sent with a select").encode('utf-8'))
        json_query = json.loads(request.GET['query'])

        fields = json_query['fields'] if 'fields' in json_query else None
        metadata_dict = json_query['where'] if 'where' in json_query else {}
        additional = json_query['additional'] if 'additional' in json_query else None

        status,payload = await self.client.select(metadata_dict,fields,additional)
        return web.Response(body=json.dumps(payload).encode('utf-8'))

    async def augselect_handler(self,request):
        if 'query' not in request.GET:
            return web.Response(body=json.dumps(
                                "'query' must be sent with a augselect").encode('utf-8'))
        json_query = json.loads(request.GET['query'])
        target = json_query['target']
        proc = json_query['proc']

        metadata_dict = json_query['where'] if 'where' in json_query else {}
        additional = json_query['additional'] if 'additional' in json_query else None
        arg = json_query['arg'] if 'arg' in json_query else None

        status,payload = await self.client.augmented_select(proc,target,arg
                                                            ,metadata_dict
                                                            ,additional)
        return web.Response(body=json.dumps(payload).encode('utf-8'))

    async def add_ts_handler(self,request):
        req_dict = await request.json()

        pk = req_dict['primary_key']
        t = ts.TimeSeries(*req_dict['ts'])
        status, payload = await self.client.insert_ts(pk,t)

        if status ==TSDBStatus.OK:
            textResp = "WriteSuccessful"
        else:
            raise Exception("Write Failed")
        return web.Response(body=json.dumps(textResp).encode('utf-8'))

    async def add_trigger_handler(self,request):
        req_dict = await request.json()
        print(req_dict)
        status, payload = await self.client.add_trigger(
                req_dict['proc'],req_dict['onwhat'],req_dict['target'], req_dict['arg'])
        if status ==TSDBStatus.OK:
            textResp = "WriteSuccessful"
        else:
            raise Exception("Write Failed")
        return web.Response(body=json.dumps(textResp).encode('utf-8'))

    async def remove_trigger_handler(self,request):
        req_dict = await request.json()
        print(req_dict)
        status, payload = await self.client.remove_trigger(
                req_dict['proc'],req_dict['onwhat'])
        if status ==TSDBStatus.OK:
            textResp = "WriteSuccessful"
        else:
            raise Exception("Write Failed")
        return web.Response(body=json.dumps(textResp).encode('utf-8'))

    async def add_metadata_handler(self,request):
        req_dict = await request.json()

        print(req_dict)
        status, payload = await self.client.upsert_meta(
                req_dict['primary_key'],req_dict['metadata_dict'])
        if status ==TSDBStatus.OK:
            textResp = "WriteSuccessful"
        else:
            raise Exception("Write Failed")
        return web.Response(body=json.dumps(textResp).encode('utf-8'))

handler = Handlers()
app = web.Application()
app.router.add_route('GET', '/tsdb', handler.homepage_handler)
app.router.add_route('GET', '/tsdb/select',handler.select_handler)
app.router.add_route('GET', '/tsdb/augselect',handler.augselect_handler)
app.router.add_route('POST', '/tsdb/add/ts', handler.add_ts_handler)
app.router.add_route('POST', '/tsdb/add/trigger', handler.add_trigger_handler)
app.router.add_route('POST', '/tsdb/remove/trigger', handler.remove_trigger_handler)
app.router.add_route('POST', '/tsdb/add/metadata', handler.add_metadata_handler)
web.run_app(app)
