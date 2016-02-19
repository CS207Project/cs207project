import reprlib
import itertools
import numpy as np

from doctest import run_docstring_examples as dtest


class TimeSeries:
    """
    Attributes
    ----------
    times : list of times that data were collected
    values: magnitudes of observations at each time


    Methods
    -------
    __init__: instantiate TimeSeries class object
    __len__: length of TimeSeries
    get_index: Helper function to get the array index of a time
    __getitem__: Returns value at a given time
    __setitem__: Set value at a given time
    __contains__: Truth value of a given time
    __repr__: Represents TimeSeries
    __str__: Returns TimeSeries as a string

    Tests
    -----
    >>> a = TimeSeries([1, 1.5, 2, 2.5, 10], [0, 2, -1, 0.5, 0])
    >>> a[2.5] = 1.0

    >>> print a[10]
    0

    >>> print a[0]
        Traceback 
        ...
        IndexError: Time not in Time Series

    >>> a.contains(1)
    True

    >>> a.contains(20)
    False

    >>> len(a)
    5

    >>> [v for v in TimeSeries([0,1,2],[1,3,5])] 
    [1,3,5]

    >>> str(a)
    returns [1.0, 1.5, 2.0, 2.5, 10.0], [0, 2, -1, 1.0, 0]

    >>> a.values()
    [0, 2, -1, 1.0, 0]

    >>> a.times()
    [1.0, 1.5, 2.0, 2.5, 10.0]

    >>> a.items()
    [(1.0, 0), (1.5, 2), (2.0, -1), (2.5, 1.0), (10.0, 0)]

    """

    def __init__(self, times, values):
        assert len(times) == len(values),"Array of Unequal Length"
        self._times = np.array(times)
        self._values = np.array(values)

    def __len__(self):
        return len(self._times)

    # // helper function to get the index of a given time
    def get_index(self,time):
        try:
            return np.where(self._times==time)[0][0]
        except IndexError:
            raise IndexError("Time not in Time Series")

    def __getitem__(self, time):
        return self._values[self.get_index(time)]

    def __setitem__(self, time, value):
        self._values[self.get_index(time)] = value
        return

    def __contains__(self, time):
        try:
            _ = self.__getitem__(time)
            return True
        except IndexError:
            return False

    def __repr__(self):
        class_name = type(self).__name__
        components = reprlib.repr(list(itertools.islice(self._times, 0, 10)))
        components2 = reprlib.repr(list(itertools.islice(self._values, 0, 10)))
        components = components[components.find('['):]
        components2 = components[components.find('['):]
        return '{}({}, {})'.format(class_name, components, components2)

    def __str__(self):
        """returns a shortened string representation of the time series"""
        components = reprlib.repr(list(itertools.islice(self._times, 0, 10)))
        components2 = reprlib.repr(list(itertools.islice(self._values, 0, 10)))
        components = components[components.find('['):]
        components2 = components[components.find('['):]
        return '{}, {}'.format(components, components2)

# Create a non-uniform TimeSeries instance:
a = TimeSeries([1, 1.5, 2, 2.5, 10], [0, 2, -1, 0.5,0.0])

# Set the value at time 2.5
print(a[2.5])
# a[2.5] = 1.0

# Set the value at time 2.5
# a[1.5] = 2.5
# print(a)

# This should return an error, because there is no time point at t=0
# a[0]

##### To run doctest:
# dtest(TimeSeries, globals(), verbose = True)
