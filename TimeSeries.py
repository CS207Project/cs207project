import reprlib
import itertools


class TimeSeries:
    """
    A class for representing a time series, initiated with data stored as a list.
    Formats data in shortened notation when printing.

    Attributes
    ----------
    data : list
        values in the timeseries


    Methods
    -------

    """

    def __init__(self, data):
        self._data = [x for x in data]

    def __len__(self):
        return len(self._data)

    def __getitem__(self, position):
        return self._data[position]

    def __setitem__(self, position, value):
        self._data[position] = value

    def __repr__(self):
        class_name = type(self).__name__
        components = reprlib.repr(list(itertools.islice(self._data, 0, 10)))
        components = components[components.find('['):]
        return '{}({})'.format(class_name, components)

    def __str__(self):
        """returns a shortened string representation of the time series"""
        components = reprlib.repr(list(itertools.islice(self._data, 0, 10)))
        components = components[components.find('['):]
        return '{}'.format(components)

a = TimeSeries(range(0, 1000000))
print("string: ", a)
print("repr: ", repr(a))

threes = TimeSeries(range(0,1000,3))
fives = TimeSeries(range(0,1000,5))

s = 0
for i in range(0,1000):
  if i in threes or i in fives:
    s += i

print("sum",s)