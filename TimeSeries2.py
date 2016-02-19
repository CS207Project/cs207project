import reprlib
import itertools
import numpy as np


class TimeSeries:
    """
    a = TimeSeries([1, 1.5, 2, 2.5, 10], [0, 2, -1, 0.5, 0])
    a[2.5] = 1.0

    print a[0]
        error

    a.contains(1)
        returns True

    a.contains(20)
        returns False

    len(a)
        returns 5

    [v for v in TimeSeries([0,1,2],[1,3,5])]
        returns [1,3,5]

    str(a)
        returns


    experiment

    """

    def __init__(self, times, values):
        assert len(times) == len(values),"Array of Unequal Length"
        self._times = np.array(times)
        self._values = np.array(values)

    @property
    def values(self):
        return self._values

    @property
    def times(self):
        return self._times

    @property
    def items(self):
        return zip(self._times,self._values)

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

    def __iter__(self):
        return iter(self._values)

    def __repr__(self):
        class_name = type(self).__name__
        components = reprlib.repr(list(itertools.islice(self._times, 0, 10)))
        components2 = reprlib.repr(list(itertools.islice(self._values, 0, 10)))
        components = components[components.find('['):]
        components2 = components[components.find('['):]
        return '{}({}, {})'.format(class_name, components, components2)

    def __str__(self):
        """
        function that returns a shortened string representation of the time series
        "[time1, time2, ...], [value1, value2, ...]"
        """
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

print(str(a))
