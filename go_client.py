#!/usr/bin/env python3
from tsdb import TSDBClient
import timeseries as ts
import numpy as np
import asyncio

from scipy.stats import norm

# m is the mean, s is the standard deviation, and j is the jitter
# the meta just fills in values for order and blarg from the schema
def tsmaker(m, s, j):
    "returns metadata and a time series in the shape of a jittered normal"
    meta={}
    meta['order'] = int(np.random.choice([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]))
    meta['blarg'] = int(np.random.choice([1, 2]))
    t = np.arange(0.0, 1.0, 0.01)
    v = norm.pdf(t, m, s) + j*np.random.randn(100)
    return meta, ts.TimeSeries(t, v)


async def run():
    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    client = TSDBClient()
    N_ts = 50
    N_vp = 5
    # add a trigger. notice the argument. It does not do anything here but
    # could be used to save a shlep of data from client to server.
    await client.add_trigger('junk', 'insert_ts', None, 'db:one:ts')
    # our stats trigger
    await client.add_trigger('stats', 'insert_ts', ['mean', 'std'], None)
    #Set up 50 time series
    mus = np.random.uniform(low=0.0, high=1.0, size=N_ts)
    sigs = np.random.uniform(low=0.05, high=0.4, size=N_ts)
    jits = np.random.uniform(low=0.05, high=0.2, size=N_ts)

    # dictionaries for time series and their metadata
    tsdict={}
    metadict={}
    for i, m, s, j in zip(range(N_ts), mus, sigs, jits):
        meta, tsrs = tsmaker(m, s, j)
        # the primary key format is ts-1, ts-2, etc
        pk = "ts-{}".format(i)
        tsdict[pk] = tsrs
        meta['vp'] = False # augment metadata with a boolean asking if this is a  VP.
        metadict[pk] = meta

    # choose 5 distinct vantage point time series
    vpkeys = ["ts-{}".format(i) for i in np.random.choice(range(N_ts), size=N_vp, replace=False)]
    for i in range(N_vp):
        # add 5 triggers to upsert distances to these vantage points
        await client.add_trigger('junk', 'insert_ts', None, 23)
        await client.add_trigger('corr', 'insert_ts', ["d_vp-{}".format(i)], tsdict[vpkeys[i]])
        # change the metadata for the vantage points to have meta['vp']=True
        metadict[vpkeys[i]]['vp']=True
    # Having set up the triggers, now inser the time series, and upsert the metadata
    for k in tsdict:
        print(tsdict[k])
        await client.insert_ts(k, tsdict[k])
        await client.upsert_meta(k, metadict[k])

    print("UPSERTS FINISHED")
    print('---------------------')
    print("STARTING SELECTS")

    print('---------DEFAULT------------')
    await client.select()

    #in this version, select has sprouted an additional keyword argument
    # to allow for sorting. Limits could also be enforced through this.
    print('---------ADDITIONAL------------')
    await client.select(additional={'sort_by': '-order'})

    print('----------ORDER FIELD-----------')
    _, results = await client.select(fields=['order'])
    for k in results:
        print(k, results[k])

    print('---------ALL FILEDS------------')
    await client.select(fields=[])

    print('------------TS with order 1---------')
    await client.select({'order': 1}, fields=['ts'])

    print('------------All fields, blarg 1 ---------')
    await client.select({'blarg': 1}, fields=[])

    print('------------order 1 blarg 2 no fields---------')
    _, bla = await client.select({'order': 1, 'blarg': 2})
    print(bla)

    print('------------order >= 4  order, blarg and mean sent back, also sorted---------')
    _, results = await client.select({'order': {'>=': 4}}, fields=['order', 'blarg', 'mean'], additional={'sort_by': '-order'})
    for k in results:
        print(k, results[k])

    print('------------order 1 blarg >= 1 fields blarg and std---------')
    _, results = await client.select({'blarg': {'>=': 1}, 'order': 1}, fields=['blarg', 'std','order'])
    for k in results:
        print(k, results[k])

    print('------------pk = ts-1 ---------')
    _, results = await client.select({'pk': 'ts-1'})
    print(len(results))

    print('------now computing vantage point stuff---------------------')
    print("VPS", vpkeys)

    #we first create a query time series.
    _, query = tsmaker(0.5, 0.2, 0.1)

    # Step 1: in the vpdist key, get  distances from query to vantage points
    # this is an augmented select
    vpdist = {}
    for v in vpkeys:
        _, results = await client.augmented_select('corr','d',query, {'pk':v})
        vpdist[v] = results[v]['d']

    #1b: choose the lowest distance vantage point
    # you can do this in local code
    print("VP DIST")
    print(vpdist)
    closest_vpk = min(vpkeys,key=lambda v:vpdist[v])

    # Step 2: find all time series within 2*d(query, nearest_vp_to_query)
    #this is an augmented select to the same proc in correlation

    _, results = await client.augmented_select('corr','d',query,
                                    {'d_'+closest_vpk: {'<=': 2*vpdist[closest_vpk]}})

    #2b: find the smallest distance amongst this ( or k smallest)
    #you can do this in local code
    nearestwanted = min(results.keys(),key=lambda p: results[p]['d'])

    # # plot the timeseries to see visually how we did.
    import matplotlib.pyplot as plt
    plt.plot(query)
    plt.plot(tsdict[nearestwanted])
    plt.show()

    ## ASK: CHECK to make sure you found the closest one (red)
    _, results = await client.augmented_select('corr','d', query)
    dists = np.array([results[k]['d'] for k in results])
    ys = np.array([1]*len(dists)) + np.random.randn(len(dists))/100
    labels = results.keys()
    colors = []

    for l in labels:
        c = 'b'
        if l in vpkeys:
            c = 'g'
        if l == nearestwanted:
            c = 'r'
        colors.append(c)

    plt.scatter(dists,ys,c=colors,s=100)
    for x,y,l in zip(dists,ys,labels):
        plt.annotate(l,xy=(x,y),xytext=(0,20)
                ,textcoords = 'offset points'
                ,rotation = 90)
    plt.show()

def main():
    loop = asyncio.get_event_loop()
    coro = asyncio.ensure_future(run())
    loop.run_until_complete(coro)#DNY: blocking call until coro completes

if __name__=='__main__':
    main()
