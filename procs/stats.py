""" This module implements the stored procedure that computes the mean and standard deviation
of a TimeSeries.

Notes
-----
proc_main
    the function called by the database on augmented selects

main
    the function called by the database on triggers
"""
import asyncio
async def main(pk, row, arg):
    """ Compute the mean and sd of a TimeSeries

    Parameters
    ----------
    pk : string or int
        this is the primary key of the row of the database
    row : dict
        dictionary consisting of column_name: value for this row in the database
    arg : anything
        optional argument passed to the function. ignored in this case

    Returns
    -------
    list
        [mean,sd] of the TimeSeries in this row of the database

    """
    return proc_main(pk,row,arg)

def proc_main(pk, row, arg):
    """ Compute the mean and sd of a TimeSeries

    Parameters
    ----------
    pk : string or int
        this is the primary key of the row of the database
    row : dict
        dictionary consisting of column_name: value for this row in the database
    arg : anything
        optional argument passed to the function. ignored in this case

    Returns
    -------
    list
        [mean,sd] of the TimeSeries in this row of the database

    """
    print("[[[[[[[[[[[STATS]]]]]]]]]]]]", pk, row, arg)
    damean = float(row['ts'].mean())
    dastd = float(row['ts'].std())
    return [damean, dastd]
