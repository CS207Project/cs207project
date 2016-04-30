""" This module implements a test stored procedure that does nothing

Notes
-----
proc_main
    the function called by the database on augmented selects. NOT IMPLEMENTED

main
    the function called by the database on triggers
"""
async def main(pk, row, arg):
    """ DO NOTHING

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
        [None]

    """
    print("[[[[[[[[[[[JUNKY]]]]]]]]]]]]", pk, row, arg)
    return [None]
