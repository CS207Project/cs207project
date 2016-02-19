import reprlib
import itertools
import numpy as np


class TimeSeries:
    """
    """

    def __init__(self, times, values):
        assert(len(times) == len(values))
        self._times = np.array(times)
        self._values = np.array(values)

    def __len__(self):
        return len(self._times)

    def get_index(self,time):
        try:
            return np.where(self._times==time)[0][0]
        except IndexError:
            raise IndexError("Time not in Time Series")

    def __getitem__(self, time):
        return self._values[get_index(time)]

    def __setitem__(self, time, value):
        self._values[get_index(time)] = value
        return

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
a = TimeSeries([1, 1.5, 2, 2.5, 10], [0, 2, -1, 0.5, 0])

# Set the value at time 2.5
print(a[2.53])
# a[2.5] = 1.0

# Set the value at time 2.5
# a[1.5] = 2.5
# print(a)

# This should return an error, because there is no time point at t=0
# a[0]
