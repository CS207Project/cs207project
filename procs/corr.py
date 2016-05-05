""" This module implements the stored procedure that computes the correlation distance metric between
a given TimeSeries argument and another TimeSeries

Notes
-----
proc_main
    the function called by the database on augmented selects

main
    the function called by the database on triggers
"""
import timeseries as ts
import numpy as np

from ._corr import stand, kernel_corr

import asyncio

# this function is directly used for augmented selects
def proc_main(pk, row, arg):
    """ Compute the kernel correlation distance of a TimeSeries to a given reference TimeSeries

    Parameters
    ----------
    pk : string or int
        this is the primary key of the row of the database
    row : dict
        dictionary consisting of column_name: value for this row in the database
    arg : list
        TimeSeries in list form to which we will compute the kerndist

    Returns
    -------
    list
        [kerndist] of the TimeSeries in this row of the database to the `arg`

    Notes
    -----
    Implementation of the kernel correlation distance is done in the _corr module

    """
    #The argument is a time series. But due to serialization it does
    #not come out as the "instance", and must be cast
    argts = ts.TimeSeries(*arg)
    #compute a standardized time series
    stand_argts = stand(argts, argts.mean(), argts.std())
    # for each row in our select/etc, standardize the time series
    stand_rowts = stand(row['ts'], row['ts'].mean(), row['ts'].std())
    #compute the normalozed kernelized cross-correlation
    kerncorr = kernel_corr(stand_rowts, stand_argts, 5)
    # compute a distance from it.
    #The distance is given by np.sqrt(K(x,x) + K(y,y) - 2*K(x,y))
    #since we are normalized the autocorrs are 1
    kerndist = np.sqrt(2*(1-kerncorr))
    print("[[[[[[[[[[[CORR]]]]]]]]]]]]",kerndist)
    return [kerndist]

#the function is wrapped in a coroutine for triggers
async def main(pk, row, arg):
    """ Compute the kernel correlation distance of a TimeSeries to a given reference TimeSeries

    Parameters
    ----------
    pk : string or int
        this is the primary key of the row of the database
    row : dict
        dictionary consisting of column_name: value for this row in the database
    arg : list
        TimeSeries in list form to which we will compute the kerndist

    Returns
    -------
    list
        [kerndist] of the TimeSeries in this row of the database to the `arg`

    Notes
    -----
    Implementation of the kernel correlation distance is done in the _corr module

    """
    return proc_main(pk, row, arg)
