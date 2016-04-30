"""
Implements a timeseries class.

Each TimeSeries object consists of a an array of times and the values recorded at those times.
We provide a lot of functionality for manupilating these time series objects.

"""
import reprlib
import itertools
import numbers
import numpy as np
import pype


class TimeSeries:
    """
    Attributes
    ----------
    times :
        list of times that data were collected
    values:
        list of magnitudes of observations at each time
    items:
        list of time, value tuples
    """

    def __init__(self, times, values):
        """instantiate TimeSeries class object

        Parameters
        ----------
        times : list like object
            the times of the TimeSeries

        values : list like object
            the values of the TimeSeries

        Returns
        -------
        TimeSeries
            new TimeSeries object
        """
        assert len(times) == len(values),"Array of Unequal Length"
        self._times = np.array(times)
        self._values = np.array(values)

    @property
    def values(self):
        "values of the TimeSeries"
        return list(self._values)

    @property
    def times(self):
        "times of the TimeSeries"
        return list(self._times)

    @property
    def items(self):
        "list of tuples of the TimeSeries"
        return list(zip(self._times,self._values))

    def __len__(self):
        "length of TimeSeries"
        return len(self._times)

    def __get_index(self,time):
        "helper function to get the index of a given time"
        if time in self.times:
            return np.where(self._times==time)[0][0]
        else:
            raise IndexError("Time not in Time Series")

    def __getitem__(self, time):
        "Dunder Method that returns value at a given time"
        return self._values[self.__get_index(time)]

    def __setitem__(self, time, value):
        "Dunder Method that Sets value at a given time"
        self._values[self.__get_index(time)] = value
        return

    def __contains__(self, time):
        "Dunder Method that gives truth value of a given time"
        return time in self._times

    def __iter__(self):
        "Dunder Method that returns an iterator over the values of the TimeSeries"
        return iter(self._values)

    def iteritems(self):
        "iterator over tuples of (time,value) in the TimeSeries"
        return zip(self._times,self._values)

    def itervalues(self):
        "iterator over values in the TimeSeries"
        return iter(self._values)

    def itertimes(self):
        "iterator over times in the TimeSeries"
        return iter(self._times)

    def __repr__(self):
        "Dunder method that gives a string representation for the programmer"
        class_name = type(self).__name__
        components = reprlib.repr(list(itertools.islice(self._times, 0, 10)))
        components2 = reprlib.repr(list(itertools.islice(self._values, 0, 10)))
        components = components[components.find('['):]
        components2 = components2[components2.find('['):]
        return '{}({}, {})'.format(class_name, components, components2)

    def __str__(self):
        """
        Dunder method that gives a shortened string representation of the TimeSeries
        [time1, time2, ...], [value1, value2, ...]

        """
        components = reprlib.repr(list(itertools.islice(self._times, 0, 10)))
        components2 = reprlib.repr(list(itertools.islice(self._values, 0, 10)))
        components = components[components.find('['):]
        components2 = components2[components2.find('['):]
        return '{}, {}'.format(components, components2)

    def __interpolate_point(self,time):
        "helper funciton for interpolation"
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
        """create a new timeseries based on interpolated values of this TimeSeries

        Parameters
        ----------
        timesList : list like object
            the times for the new interpolated TimeSeries

        Returns
        -------
        TimeSeries
            new TimeSeries object who's times are `timesList`
        """
        valuesList = [self.__interpolate_point(time) for time in timesList]
        return TimeSeries(timesList,valuesList)

    def median(self):
        "compute the median of the values of a TimeSeries"
        if len(self) == 0:
            raise ValueError("Cannot calculate median of empty TimeSeries.")
        return np.median(self.values)

    def __timeEqual(self, other):
        "helper that checks if two TimeSeries have the same times"
        # try:
        return (len(self.times) == len(other.times) and
        all(a==b for a,b in zip(self.times, other.times)))
        # except(AttributeError):
        #     raise NotImplemented

    def __try_wrapper(f):
        def inner(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except(AttributeError):
                raise NotImplementedError
        return inner

    @__try_wrapper
    def __eq__(self, other):
        """Dunder function to check if two TimeSeries are equal

        Parameters
        ----------
        other : TimeSeries object
            another TimeSeries
        Returns
        -------
        bool
            truth value of this and the other TimeSeries being equal
        """
        if self.__timeEqual(other):
            return all(a==b for a,b in zip(self.values, other.values))
        else:
            raise ValueError(str(self)+' and '+str(other)+' must have the same time points')

    @pype.component
    def __add__(self, rhs):
        """Dunder function to add two TimeSeries

        Parameters
        ----------
        rhs : TimeSeries object
            another TimeSeries

        Returns
        -------
        TimeSeries
            sum of two TimeSeries

        Raises
        ------
        ValueError
            if the times of the two TimeSeries are not the same
        """
        try:
            if (self.__timeEqual(rhs)):
                pairs = zip(self.values, rhs.values)
                return TimeSeries(self.times, [a + b for a, b in pairs])
            else:
                raise ValueError(str(self)+' and '+str(rhs)+' must have the same time points')
        except(AttributeError):
            raise NotImplementedError

    @pype.component
    def __sub__(self, rhs):
        """Dunder function to subtract two TimeSeries

        Parameters
        ----------
        rhs : TimeSeries object
            another TimeSeries

        Returns
        -------
        TimeSeries
            this TimeSeries minus the other

        Raises
        ------
        ValueError
            if the times of the two TimeSeries are not the same
        """
        if isinstance(rhs,TimeSeries):
            try:
                if (self.__timeEqual(rhs)):
                    pairs = zip(self.values, rhs.values)
                    return TimeSeries(self.times, [a - b for a, b in pairs])
                else:
                    raise ValueError(str(self)+' and '+str(rhs)+' must have the same time points')
            except(AttributeError):
                raise NotImplementedError
        else:
            return TimeSeries(self.times, self.values - rhs)

    @pype.component
    def __mul__(self, rhs):
        """Dunder function to multiply a TimeSeries with a number or another TimeSeries

        Parameters
        ----------
        rhs : TimeSeries object or a number
            the TimeSeries or number that you want to use

        Returns
        -------
        TimeSeries
            this TimeSeries times the rhs

        Raises
        ------
        ValueError
            if the times of the two TimeSeries are not the same

        Notes
        -----
            if `rhs` is a number then values are values * rhs. if `rhs` is a TimeSeries then we perform an elementwise product
        """
        if isinstance(rhs,numbers.Integral):
            return TimeSeries(self.times,[a*rhs for a in self.values])
        try:
            if (self.__timeEqual(rhs)):
                pairs = zip(self.values, rhs.values)
                return TimeSeries(self.times, (a * b for a, b in pairs))
            else:
                raise ValueError(str(self)+' and '+str(rhs)+' must have the same time points')
        except(AttributeError):
            raise NotImplementedError

    @pype.component
    def __abs__(self):
        """Dunder function to get the L2 norm of the values

        Returns
        -------
        double
            L2 norm

        """
        return np.sqrt(sum(x * x for x in self.values))

    @pype.component
    def __bool__(self):
        """Dunder function to check if abs value of the TimeSeries is > 0

        Returns
        -------
        bool
            truth value of abs of TimeSeries > 0

        """
        return bool(abs(self))

    @pype.component
    def __neg__(self):
        """Dunder function that negates the values of a TimeSeries

        Returns
        -------
        TimeSeries
            same times, - the values

        """
        return TimeSeries(self.times, [-x for x in self.values])

    @pype.component
    def __pos__(self):
        """Dunder function that returns the same TimeSeries

        Returns
        -------
        TimeSeries
            identity

        """
        return TimeSeries(self.times, self.values)

    @pype.component
    def __truediv__(self,rhs):
        """Dunder function to divide this TimeSeries by a number or another TimeSeries

        Parameters
        ----------
        rhs : TimeSeries object or a number
            the TimeSeries or number that you want to use

        Returns
        -------
        TimeSeries
            this TimeSeries / the rhs

        Raises
        ------
        ValueError
            if the times of the two TimeSeries are not the same

        Notes
        -----
            if `rhs` is a number then values are values / rhs. if `rhs` is a v then we perform an elementwise division
        """
        if isinstance(rhs,TimeSeries):
            try:
                if (self.__timeEqual(rhs)):
                    pairs = zip(self.values, rhs.values)
                    return TimeSeries(self.times, (a / b for a, b in pairs))
                else:
                    raise ValueError(str(self)+' and '+str(rhs)+' must have the same time points')
            except(AttributeError):
                raise NotImplementedError
        else:
            return TimeSeries(self.times,[a/rhs for a in self.values])

    # need to add tests!!
    @pype.component
    def std(self):
        """Standard Deviation of a TimeSeries

        Returns
        -------
        double
            standard dev of values

        Raises
        ------
        ValueError
            if the length is < 2

        """
        if len(self) < 2:
            raise ValueError("Cannot calculate std of a TimeSeries of length %d"
                ,len(self.values))
        return np.std(self.values)

    # need to add tests!!
    @pype.component
    def mean(self):
        """Mean of a TimeSeries

        Returns
        -------
        double
            mean of values

        Raises
        ------
        ValueError
            if the TimeSeries is empty

        """
        if len(self) == 0:
            raise ValueError("Cannot calculate mean of empty TimeSeries.")
        return np.average(self.values)

    def to_json(self):#DNY: to interface with TSDB objects
        #ASK: fixing DNY's implementation (times need to be first)
        """Converts this TimeSeries to a list of lists so that it can be converted to json

        Returns
        -------
        list
            [[times],[values]] of this TimeSeries

        Notes
        -----
        DNY
            to interface with TSDB objects
        ASK
            fixing DNY's implementation (times need to be first)

        """
        return [[float(i) for i in self.times],[float(i) for i in self.values]]

    @classmethod
    def from_json(cls,dataList):
        """Converts a list of lists to a TimeSeries object

        Parameters
        ----------
        dataList : list
            [[times],[values]] that will form this TimeSeries

        Returns
        -------
        TimeSeries
            the resulting TimeSeries

        """
        return cls(dataList[0],dataList[1])

##### To run doctest:
# dtest(TimeSeries, globals(), verbose = True)
