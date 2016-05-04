"""Vantage Point Trees and related code.

The structure of these trees is that each non-leaf node is a vantage point and each
leaf node is contains a group of pks that are possibly the closest ones to our query.

Due to the tree structure we perform log n distance calculations
(assuming the tree is balanced)
"""

import bintrees
import numpy as np
import uuid
from graphviz import Digraph
import matplotlib.pyplot as plt

MAX_NODES = 10000

class VPNode():
    """Node of a vantage point tree
    """
    def __init__(self):
        self.parent = None
        self.left_child = None
        self.right_child = None

    def preorder(self):
        if self.left_child is None and self.right_child is None:
            return [(self,None,None)]
        else:
            return [(self, self.left_child, self.right_child)] + self.left_child.preorder() + self.right_child.preorder()


class VPTreeNonLeaf(VPNode):
    """This represents a vantage point
    """
    def __init__(self, uid, pk, median_dist, left_child = None, right_child = None):
        super().__init__()
        self.uid = uid
        self.pk = pk
        self.median_dist = median_dist
        self.left_child = left_child
        self.right_child = right_child

class VPTreeLeaf(VPNode):
    """This represents a node that contains the list of possible candidates
    as the closest
    """
    def __init__(self,pk_list,uid):
        super().__init__()
        self.pk_list = pk_list
        self.uid = uid

class VPTree:
    def __init__(self, pks, vp_pks, dist_func):
        self.vps_pks = vp_pks
        self.dist_func = dist_func
        self.root = self.makeVPTree(pks, vp_pks)

    def dot(self):
        """Create a graphviz dot file to visualize the tree
        """
        d = Digraph(comment="VP Tree")
        for parent, left, right in self.root.preorder():

            if isinstance(parent,VPTreeNonLeaf):
                d.node(str(parent.uid), """VP Node:: Key={} Median Dist = {:2.2f}
                                        """.format(parent.pk, parent.median_dist))
                d.edge(str(parent.uid), str(left.uid))
                d.edge(str(parent.uid), str(right.uid))
            elif isinstance(parent,VPTreeLeaf):
                d.node(str(parent.uid), "Leaf Node:: "+str(parent.pk_list))
            else:
                raise Exception("something went wrong")

        return d

    def makeVPTree(self, pks, vp_pks):
        """Make a vantage point tree

        Parameters
        ----------
        pks : list
            list of primary keys
        vp_pks : list
            list of primary keys to be used as vantage points
        dist_func : function
            takes a vp_key and a list of pks and returns distances
        """
        # id for this node
        uid = uuid.uuid1().int % MAX_NODES

        # if there aren't any vantage points left, return the pks
        # that we have left as a leaf node
        if vp_pks == []:
            return VPTreeLeaf(pks,uid)
        else:
            # pick a vp at random
            vp = vp_pks[np.random.choice(np.arange(len(vp_pks)))]

            # compute distance to all points and find median
            vp_dist = self.dist_func(vp, pks)
            M = np.median(vp_dist)

            # loop through distances and assign to left or right node
            l_pks, l_vp_pks, r_pks, r_vp_pks = [],[],[],[] # placeholders
            for p,d in zip(pks,vp_dist):
                if d < M:
                    l_pks.append(p)
                    if p in vp_pks and p != vp:
                        l_vp_pks.append(p)
                else:
                    r_pks.append(p)
                    if p in vp_pks and p != vp:
                        r_vp_pks.append(p)

            # recursively comptute the children
            left_child = self.makeVPTree(l_pks, l_vp_pks)
            right_child = self.makeVPTree(r_pks, r_vp_pks)

            # make the root node
            this = VPTreeNonLeaf(uid, vp, M, left_child,right_child)
            left_child.parent = this
            right_child.parent = this
            return this

    def getCloseSubset(self, arg, dist_arg):
        """Get the subset of nodes that can be the closest to this argument

        Parameters
        ----------
        arg : anything
            query argument
        dist_arg : function
            takes a primary key and the arg and returns the distance between them
        """

        curr = self.root
        while not isinstance(curr,VPTreeLeaf):
            d = dist_arg(curr.pk, arg)
            if d < curr.median_dist:
                curr = curr.left_child
            else:
                curr = curr.right_child

        return curr.pk_list

if __name__ == "__main__":
    np.random.seed(12345)

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
    d.render("test",view=T)

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

    # plot : the red point should be the one on the far left
    colors = []
    for l in pks:
        c = 'b'
        if l in group:
            c = 'g'
        if l == nearestwanted:
            c = 'r'
        colors.append(c)

    plt.scatter(dists,ys,c=colors,s=100)
    for x,y,l in zip(dists,ys,pks):
        plt.annotate(l,xy=(x,y),xytext=(0,20)
                ,textcoords = 'offset points'
                ,rotation = 90)
    plt.show()
