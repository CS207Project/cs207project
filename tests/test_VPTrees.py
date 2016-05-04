from vptrees import *
from graphviz import Digraph
import unittest
import numpy as np

class VPTreesTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_main(self):
        points = {'a'+str(i) : np.random.normal(0,10) for i in range(100)}
        vps = ['a1','a5','a40','a39','a99','a75','a2']

        def dist(vp,pks):
            x = points[vp]
            y = np.array([points[p] for p in pks])
            return np.abs(x-y)

        def dist_arg(vp,arg):
            x = points[vp]
            return np.abs(x-arg)

        pks = list(points.keys())
        t = VPTree(pks, vps, dist)
        d = t.dot()

        # print graphiz graph
        # d.render("test",view=True)

        ########## check if this is working
        query = np.random.normal(0,10) # query point

        # true distances from query to all the points
        dists = np.array([np.abs(query - points[p]) for p in pks])
        ys = np.array([1]*len(dists)) + np.random.randn(len(dists))/100

        # this is the test. group returns a subset of possible close points
        group = t.getCloseSubset(query,dist_arg)
        nearestwanted = min(pks, key = lambda p:dists[pks.index(p)])

        ######################
        assert nearestwanted in group
        #######################

if __name__ == '__main__':
    unittest.main()
