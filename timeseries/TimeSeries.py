import reprlib
import itertools
import numbers
import numpy as np
import pype


class TimeSeries:
    """
    Properties
    ----------
    times : list of times that data were collected
    values: list of magnitudes of observations at each time
    items: list of time, value tuples

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

    Tests are in the Test.py file
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
        return time in self._times

    def __iter__(self):
        return iter(self._values)

    def iteritems(self):
        return zip(self._times,self._values)

    def itervalues(self):
        return iter(self._values)

    def itertimes(self):
        return iter(self._times)

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
        "Interpolates time points within times series based on submitted data"
        if not isinstance(timesList, list):
            raise TypeError("times list must be a list of floats")
        valuesList = [self.__interpolate_point(float(time)) for time in timesList]
        return TimeSeries(timesList,valuesList)

    def median(self):
        "calculates the median value of the times series"
        if len(self) == 0:
            raise ValueError("Cannot calculate median of empty timeseries.")
        return np.median(self.values)

    def __timeEqual(self, other):
        "helper function to determin equality of times array of timeseries"
        return (len(self.times) == len(other.times) and
        all(a==b for a,b in zip(self.times, other.times)))
        # except(AttributeError):
        #     raise NotImplemented

    def __try_wrapper(f):
        "Wrapper to standardize the error upon wrong inputs"
        def inner(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except(AttributeError):
                raise NotImplementedError
        return inner

    @__try_wrapper
    def __eq__(self, other):
        if not isinstance(other, TimeSeries):
            return TypeError("TimeSeries can only be equal with other TimeSeries Instances")
        if self.__timeEqual(other):
            return all(a==b for a,b in zip(self.values, other.values))
        else:
            return False
            #raise ValueError(str(self)+' and '+str(other)+' must have the same time points')

    @pype.component
    def __add__(self, rhs):
        # DNY: Could Refactor into
        try:
            if isinstance(rhs, numbers.Real):
                return TimeSeries(self.times, [v + rhs for v in self.values])
            elif isinstance(rhs, TimeSeries):
                if (self.__timeEqual(rhs)):
                    pairs = zip(self.values, rhs.values)
                    return TimeSeries(self.times, [a + b for a, b in pairs])
                else:
                    raise ValueError(str(self)+' and '+str(rhs)+' must have the same time points')
            elif isinstance(rhs, np.ndarray) or isinstance(rhs, list):
                raise AttributeError
            else:
                raise AttributeError
        except(AttributeError):
            raise NotImplementedError

    def __radd__(self, lhs):
        "__radd__ delegates to __add__ to handle addition"
        return self + lhs

    @pype.component
    def __sub__(self, rhs):
        try:
            if isinstance(rhs, numbers.Real):
                return TimeSeries(self.times, [v - rhs for v in self.values])
            elif isinstance(rhs, TimeSeries):
                if (self.__timeEqual(rhs)):
                    pairs = zip(self.values, rhs.values)
                    return TimeSeries(self.times, [a - b for a, b in pairs])
                else:
                    raise ValueError(str(self)+' and '+str(rhs)+' must have the same time points')
            elif isinstance(rhs, np.ndarray) or isinstance(rhs, list):
                raise AttributeError
            else:
                raise AttributeError
        except(AttributeError):
            raise NotImplementedError("Must submit either a TimeSeries or a numbers.Real instance")

    def __rsub__(self, lhs):
        "__rsub__ delegates to __sub__ to handle subtraction"
        return -(self - lhs)

    @pype.component
    def __mul__(self, rhs):
        try:
            if isinstance(rhs, numbers.Real):
                return TimeSeries(self.times, [v * rhs for v in self.values])
            elif isinstance(rhs, TimeSeries):
                if (self.__timeEqual(rhs)):
                    pairs = zip(self.values, rhs.values)
                    return TimeSeries(self.times, [a * b for a, b in pairs])
                else:
                    raise ValueError(str(self)+' and '+str(rhs)+' must have the same time points')
            elif isinstance(rhs, np.ndarray) or isinstance(rhs, list):
                raise AttributeError
            else:
                raise AttributeError
        except(AttributeError):
            raise NotImplementedError

    def __rmul__(self, lhs):
        "__rmul__ delegates to __mul__ to handle multiplication"
        return self * lhs

    @pype.component
    def __abs__(self):
        return np.sqrt(sum(x * x for x in self.values))

    @pype.component
    def __bool__(self):
        return bool(abs(self))

    @pype.component
    def __neg__(self):
        return TimeSeries(self.times, [-x for x in self.values])

    @pype.component
    def __pos__(self):
        return TimeSeries(self.times, self.values)

    @pype.component
    def __truediv__(self,rhs):
        try:
            if isinstance(rhs, numbers.Real):
                return TimeSeries(self.times, [v / rhs for v in self.values])
            elif isinstance(rhs, TimeSeries):
                if (self.__timeEqual(rhs)):
                    pairs = zip(self.values, rhs.values)
                    return TimeSeries(self.times, [a / b for a, b in pairs])
                else:
                    raise ValueError(str(self)+' and '+str(rhs)+' must have the same time points')
            elif isinstance(rhs, np.ndarray) or isinstance(rhs, list):
                raise AttributeError
            else:
                raise AttributeError
        except(AttributeError):
            raise NotImplementedError

    def __rtruediv__(self,rhs):
        raise NotImplementedError

    # need to add tests!!
    @pype.component
    def std(self):
        if len(self) < 2:
            raise ValueError("Cannot calculate std of a timeseries of length %d"
                ,len(self.values))
        return np.std(self.values)

    # need to add tests!!
    @pype.component
    def mean(self):
        if len(self) == 0:
            raise ValueError("Cannot calculate mean of empty timeseries.")
        return np.average(self.values)

    def to_json(self):#DNY: to interface with TSDB objects
        #ASK: fixing DNY's implementation (times need to be first)
        return [[float(i) for i in self.times],[float(i) for i in self.values]]

    @classmethod
    def from_json(cls,dataList):
        return cls(dataList[0],dataList[1])

##### To run doctest:
# dtest(TimeSeries, globals(), verbose = True)
