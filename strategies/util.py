""" This package provides common utility for strategies"""

import numpy as np

def read_to_matrix(file_name):
    """ Read a spaace separated file to a matrix.

        Args:
            file_name: String. Name of the file to read.

        Returns:
            mat: numpy.matrix. The matrix read from the file.
    """
    with open(file_name, 'r') as file_handle:
        content = file_handle.read()

    content = content.replace('\n', ';')
    # Get rid of the last ';' bofore converting to matrix.
    mat = np.mat(content[:-1])
    return mat
