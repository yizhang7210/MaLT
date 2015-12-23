""" This module provides common utility for strategies"""

import numpy as np


#====================================================================
#   Functions:
#====================================================================

def read_to_matrix(file_name):
    """ Read a space or comma separated file to a matrix.

        Args:
            file_name: String. Name of the file to read.

        Returns:
            mat: np.matrix. The matrix read from the file.
    """
    with open(file_name, 'r') as file_handle:
        content = file_handle.read()

    content = content.replace('\n', ';')

    # Get rid of the last ';' bofore converting to matrix.
    mat = np.mat(content[:-1])
    return mat


def price_to_pip(price, pip_multiplier):
    """ Numbers are format to 1 decimal places in pips.

        Args:
            price: Float. Actual price of instrument.
            pip_multiplier: int. The multiplier for calculating pip from price.

        Returns:
            The price in pips with 1 decimal place.
    """
    pip = price * pip_multiplier
    return "{0:.1f}".format(pip)


def list_to_float(lst):
    """ Change the entire list to float.

        Args:
            lst: List of Strings.

        Returns:
            List of Floats. The values in Floats.
    """
    return [float(x) for x in lst]


def get_pip_multiplier(instrument):
    """ Obtain the price to pip multiplier. It's usually 10000, in
        various currency pairs involving JPY, it could be 100.

        Args:
            instrument: String. Instrument of interest. e.g. EUR_USD.

        Returns:
            multiplier: int. Either 100 or 10000, depends on the instrument.
    """
    if instrument in ['USD_JPY']:
        return 100
    else:
        return 10000

