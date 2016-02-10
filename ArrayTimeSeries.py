import itertools
import numpy as np
#from TimeSeries import TimeSeries


class ArrayTimeSeries():
    """
    A class for representing a time series,
    initiated with data stored as a numpy array.
    Formats data in shortened notation when printing.

    Attributes
    ----------
    data : list
        values in the timeseries


    Methods
    -------

    """

    def __init__(self, data):
        self._data = np.array(data)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, position):
        return self._data[position]

    def __setitem__(self, position, value):
        self._data[position] = value

    def __repr__(self):
        class_name = type(self).__name__
        return "{}({})".format(class_name, self._data[1:5])

    def __str__(self):
        class_name = type(self).__name__
        return "{}".format(self._data[1:5])

threes = ArrayTimeSeries(range(0, 1000, 3))
fives = ArrayTimeSeries(range(0, 1000, 5))
print(repr(threes))
print(fives)


s = 0
for i in range(0, 1000):
    if i in threes or i in fives:
        s += i

print("sum", s)
