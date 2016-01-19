""" This module is responsible for defining the base strategy class as well as
    providing shared utilities across the strategy package.
"""

import common
import numpy as np

#===============================================================================
#   Classes:
#===============================================================================

class BaseStrategy(object):
    """ Base class in strategies package. Responsible for defining the basic
        properties of strategy classes.
    """

    def __init__(self, instrument):
        """ Initialize the BaseStrategy class.

            Args:
                instrument: string. The currency pair. e.g. 'EUR_USD'.

            Returns:
                void.
        """
        self.instrument = instrument
        self.pip_factor = common.get_pip_factor(instrument)
        self.params = {}

        return


    def get_params(self):
        """ Get parameters for this strategy.

            Args:
                void.

            Returns:
                self.params: dict. Key-value pairs for this strategy.
        """
        return self.params


    def set_params(self, **params):
        """ Abstract method for setting parameters for this strategy."""
        pass


    def execute(self, executor, info):
        """ Abstract method for executing the strategy on a daily basis."""
        pass


    def serialize(self):
        """ Abstract method for serialize the strategy."""
        pass


    def get_best(self):
        """ Abstract method for getting the best instance of this strategy."""
        pass


#===============================================================================
#   Functions:
#===============================================================================

def read_features(input_file):
    """ Read a space or comma separated file to a matrix.

        Args:
            input_file: string. Name of the file to read.

        Returns:
            mat: np.matrix. The matrix read from the file.
    """
    with open(input_file, 'r') as file_handle:
        content = file_handle.read()

    content = content.replace('\n', ';')

    # Get rid of the last trailing ';' bofore converting to matrix.
    mat = np.matrix(content[:-1])

    return mat


