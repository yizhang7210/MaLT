""" This module provides common utility for strategies"""

import numpy as np


#===============================================================================
#   Functions:
#===============================================================================

def read_to_matrix(file_name):
    """ Read a space or comma separated file to a matrix.

        Args:
            file_name: string. Name of the file to read.

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
            price: float. Actual price of instrument.
            pip_multiplier: int. The multiplier for calculating pip from price.

        Returns:
            The price in pips with 1 decimal place.
    """
    pip = price * pip_multiplier
    return "{0:.1f}".format(pip)


def list_to_float(lst):
    """ Change the entire list to float.

        Args:
            lst: list of Strings.

        Returns:
            list of floats. The values in floats.
    """
    return [float(x) for x in lst]


def get_pip_multiplier(instrument):
    """ Obtain the price to pip multiplier. It's usually 10000, in
        various currency pairs involving JPY, it could be 100.

        Args:
            instrument: string. Instrument of interest. e.g. EUR_USD.

        Returns:
            multiplier: int. Either 100 or 10000, depends on the instrument.
    """
    if instrument in ['USD_JPY']:
        return 100
    else:
        return 10000


def build_tree_params():
    """ Build a list of dictionaries that can be used for setting parameters
        for a DecisionTreeRegressor or DecisionTreeClassifier in sklearn.tree.

        Args:
            void.

        Returns:
            lst: list of dictionaries. Each entry a valid parameter set.
    """
    lst = [{'max_depth': x, 'min_samples_split': y, 'threshold': z} for x in \
          range(4, 11, 2) for y in range(2, 21, 4) for z in range(0, 101, 20)]

    return lst











