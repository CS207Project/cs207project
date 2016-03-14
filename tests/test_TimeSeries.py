import unittest
from timeseries import TimeSeries

class TSTests(unittest.TestCase):
    """
    This class contains all the tests for the time series class

    Tests
    -----
    >>> a = TimeSeries([1, 1.5, 2, 2.5, 10], [0, 2, -1, 0.5, 0])
    >>> a[2.5] = 1.0 # // test for setting

    >>> str(a) # // test string representation
    '[1.0, 1.5, 2.0, 2.5, 10.0], [0.0, 2.0, -1.0, 1.0, 0.0]'

    >>> print(a[10]) # // test string indexing
    0.0

    >>> 1 in a
    True

    >>> 20 in a
    False

    >>> [v for v in TimeSeries([0,1,2],[1,3,5])]
    [1, 3, 5]

    >>> len(a)
    5

    >>> str(a)
    '[1.0, 1.5, 2.0, 2.5, 10.0], [0.0, 2.0, -1.0, 1.0, 0.0]'

    >>> a.values
    [0.0, 2.0, -1.0, 1.0, 0.0]

    >>> a.times
    [1.0, 1.5, 2.0, 2.5, 10.0]

    >>> a.items
    [(1.0, 0.0), (1.5, 2.0), (2.0, -1.0), (2.5, 1.0), (10.0, 0.0)]

    """
    def test_interpolate1(self):
        a = TimeSeries([0,5,10], [1,2,3])

        self.assertEqual(a.interpolate([-100,100]),TimeSeries([-100, 100], [1, 3]))

    def test_interpolate2(self):
        a = TimeSeries([0,5,10], [1,2,3])
        b = TimeSeries([2.5,7.5], [100, -100])

        self.assertEqual(a.interpolate(b.times),TimeSeries([2.5, 7.5], [1.5, 2.5]))

    def test_interpolate3(self):
        a = TimeSeries([0,5,10], [1,2,3])
        b = TimeSeries([2.5,7.5], [100, -100])

        self.assertEqual(a.interpolate([1]),TimeSeries([1], [1.2]))

    def test_emptyMedian(self):
        t2 = TimeSeries([], [])

        with self.assertRaises(ValueError):
            t2.median()

    def test_emptyMean(self):
        t2 = TimeSeries([], [])

        with self.assertRaises(ValueError):
            t2.mean()

    def test_mean(self):
        t1 = TimeSeries([1, 2, 3, 4], [40, 50, 60, 70])

        self.assertEqual(t1.mean(),55.0)

    def test_median(self):
        t1 = TimeSeries([1, 2, 3, 4], [40, 50, 60, 70])

        self.assertEqual(t1.median(),55.0)

    def test_add_sub_mul(self):
        t1 = TimeSeries([1, 2, 3, 4], [40, 50, 60, 70])
        t2 = TimeSeries([1, 2, 3, 4], [40, 50, 60, 70])
        self.assertEqual(t1 + t2 - t1 ,t1*1)

    def test_pos_neg(self):
        t1 = TimeSeries([1, 2, 3, 4], [40, 50, 60, 70])
        self.assertEqual(-(-t1), + t1)

    def test_abs(self):
        t1 = TimeSeries([1, 2], [3, 4])
        self.assertEqual(abs(t1),5)

    def test_bool(self):
        t1 = TimeSeries([1, 2], [3, 4])
        self.assertEqual(bool(t1),True)

    def test_iteritems(self):
        t1 = TimeSeries([1, 2], [3, 4])
        self.assertEqual(list(t1.itertimes()),[1,2])

    def test_itervalues(self):
        t1 = TimeSeries([1, 2], [3, 4])
        self.assertEqual(list(t1.itervalues()),[3,4])
