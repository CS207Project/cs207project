import asyncio
from aiohttp import web
from tsdb import TSDBClient
import timeseries as ts
import json

class Handlers:
    def __init__(self):
        self.client = TSDBClient()
        pass

    async def homepage_handler(self,request):
        body_txt = """
        RESTful API Implementation:

        / --> homepage describing the API
        /test --> creates some test time series to run tests
        /tsdb/select --> select's columns from the DB based on criteria

        Usage:
        select : select?fields=field1&fields=field2&metadata_dict=column:value

        Examples:
        1> http://localhost:8080/tsdb/select?metadata_dict=order:2&fields=[] --> show all the fields (except for ts) where order == 2
        2> http://localhost:8080/tsdb/select?metadata_dict=order:2&fields=ts --> show only ts where order == 2
        3> http://localhost:8080/tsdb/select?metadata_dict=order:2&fields=ts&fields=blarg --> show ts and blarg where order == 2
        4> http://localhost:8080/tsdb/select?fields=[] --> show all the non-ts fields for all timeseries

        """
        return web.Response(body=body_txt.encode('utf-8'))
    async def test_upserts_handler(self,request):
        await self.client.add_trigger('junk', 'insert_ts', None, 23)#DNY: looks for junk.py in procs/ directory
        await self.client.add_trigger('junk', 'select', None, 23)
        await self.client.add_trigger('stats', 'insert_ts', ['mean', 'std'], None)
        await self.client.insert_ts('one',ts.TimeSeries([1, 2, 3],[1, 4, 9]))
        await self.client.insert_ts('two',ts.TimeSeries([2, 3, 4],[4, 9, 16]))
        await self.client.insert_ts('three',ts.TimeSeries([9,3,4],[4,0,16]))
        await self.client.remove_trigger('junk', 'insert_ts')
        await self.client.insert_ts('four',ts.TimeSeries([0,0,4],[1,0,4]))
        await self.client.upsert_meta('one', {'order': 1, 'blarg': 1})
        await self.client.upsert_meta('two', {'order': 2})
        await self.client.upsert_meta('three', {'order': 1, 'blarg': 2})
        await self.client.upsert_meta('four', {'order': 2, 'blarg': 2})
        return web.Response(body=b"Upserts Done")

    async def select_handler(self,request):
        metadata_dict = {}
        fields = None
        for k,v in request.GET.items():
            if k == 'metadata_dict':
                column,value = v.split(':')
                metadata_dict[column] = value
            if k == 'fields':
                if fields is None:
                    fields = []
                if v != '[]':
                    fields.append(v)
        # status,payload = await self.client.select({'order': 1}, fields=['ts'])
        status,payload = await self.client.select(metadata_dict,fields)
        return web.Response(body=json.dumps(payload).encode('utf-8'))

handler = Handlers()
app = web.Application()
app.router.add_route('GET', '/', handler.homepage_handler)
app.router.add_route('GET', '/tsdb/test', handler.test_upserts_handler)
app.router.add_route('GET','/tsbd/select',handler.select_handler)

web.run_app(app)
