import reprlib
import itertools
import numpy as np


class TimeSeries:
    """
    """

    def __init__(self, times, values):
        self._times = np.array(times)
        self._values = np.array(values)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, position):  # not working
        return self._values[self._time[position]]

    def __setitem__(self, position, value):
        self._values[position] = value

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

a = TimeSeries([1, 1.5, 2, 2.5, 10], [0, 2, -1, 0.5, 0])
print(a)
a[2.5] == 0.5
a[1.5] = 2.5
print(a)
print(a[2.5])
print(a[0])
