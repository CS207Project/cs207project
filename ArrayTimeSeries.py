import itertools
import numpy as np
from TimeSeries import TimeSeries


class ArrayTimeSeries(TimeSeries):
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

# smoke test
# threes = ArrayTimeSeries(range(0, 1000, 3))
# fives = ArrayTimeSeries(range(0, 1000, 5))
# print(repr(threes))
# print(fives)


# s = 0
# for i in range(0, 1000):
#     if i in threes or i in fives:
#         s += i

# print("sum", s)
