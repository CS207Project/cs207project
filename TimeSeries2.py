import reprlib
import itertools
import numpy as np

from doctest import run_docstring_examples as dtest


class TimeSeries:
    """
    Properties
    ----------
    times : list of times that data were collected
    values: list of magnitudes of observations at each time
    itemes: list of time, value tuples

    Methods
    -------
    __init__: instantiate TimeSeries class object
    __len__: length of TimeSeries
    __get_index: Helper function to get the array index of a time
    __getitem__: Returns value at a given time
    __setitem__: Set value at a given time
    __contains__: Truth value of a given time
    __repr__: Represents TimeSeries
    __str__: Returns TimeSeries as a string

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

    >>> a = TimeSeries([0,5,10], [1,2,3])
    >>> b = TimeSeries([2.5,7.5], [100, -100])

    >>> a.interpolate([1])
    TimeSeries([1], [1.2])

    >>> a.interpolate(b.times)
    TimeSeries([2.5, 7.5], [1.5, 2.5])

    >>> a.interpolate([-100,100])
    TimeSeries([-100, 100], [1, 3])
    """

    def __init__(self, times, values):
        assert len(times) == len(values),"Array of Unequal Length"
        self._times = np.array(times)
        self._values = np.array(values)

    @property
    def values(self):
        return list(self._values)

    @property
    def times(self):
        return list(self._times)

    @property
    def items(self):
        return list(zip(self._times,self._values))

    def __len__(self):
        return len(self._times)

    # // helper function to get the index of a given time
    def __get_index(self,time):
        if time in self.times:
            return np.where(self._times==time)[0][0]
        else:
            raise IndexError("Time not in Time Series")

    def __getitem__(self, time):
        return self._values[self.__get_index(time)]

    def __setitem__(self, time, value):
        self._values[self.__get_index(time)] = value
        return

    def __contains__(self, time):
        if time in self._times:
            return True
        else:
            return False

    def __iter__(self):
        return iter(self._values)

    def __repr__(self):
        class_name = type(self).__name__
        components = reprlib.repr(list(itertools.islice(self._times, 0, 10)))
        components2 = reprlib.repr(list(itertools.islice(self._values, 0, 10)))
        components = components[components.find('['):]
        components2 = components2[components2.find('['):]
        return '{}({}, {})'.format(class_name, components, components2)

    def __str__(self):
        """
        function that returns a shortened string representation of the time series
        "[time1, time2, ...], [value1, value2, ...]"
        """
        components = reprlib.repr(list(itertools.islice(self._times, 0, 10)))
        components2 = reprlib.repr(list(itertools.islice(self._values, 0, 10)))
        components = components[components.find('['):]
        components2 = components2[components2.find('['):]
        return '{}, {}'.format(components, components2)

    def __interpolate_point(self,time):
        if time in self.times:
            return self[time]
        else:
            # check endpoints
            if time < self.times[0]:
                return self.values[0]
            elif time > self.times[-1]:
                return self.values[-1]
            else:
                # get closest values on either side
                aboveTime = self._times[self._times>time].min()
                belowTime = self._times[self._times<time].max()

                # linearly interpolate
                slope = (self[aboveTime] - self[belowTime])/float(aboveTime - belowTime)
                intercept = (self[belowTime]*aboveTime - self[aboveTime]*belowTime) \
                                / (aboveTime - belowTime)
                return slope * time + intercept

    def interpolate(self,timesList):
        valuesList = [self.__interpolate_point(time) for time in timesList]
        return TimeSeries(timesList,valuesList)

##### To run doctest:
# dtest(TimeSeries, globals(), verbose = True)
