""" This is the malt.strategies.euler.test.test_transformer module.
    This module is responsible for testing malt.strategies.euler.transformer.
"""

# External imports
import csv
import os
import unittest

# Internal imports
from malt import common
from malt.strategies.euler import transformer

#===============================================================================
# Classes:
#===============================================================================

class TestTransformer(unittest.TestCase):
    """ Class for testing transformer."""

    def setUp(self):
        """ Set up temporary files."""
        self.tmp_file = "tmp.csv"

        return


    def tearDown(self):
        """ Delete temporary files."""
        if os.path.isfile(self.tmp_file):
            os.remove(self.tmp_file)

        return


    def test_transformation(self):
        """ Test the data gets transformed and written properly."""
        # Pick the path and transform the data.
        in_file = common.get_raw_data("USD_CHF")
        out_file = self.tmp_file
        transformer.transform(in_file, out_file, 10000)

        # Read the file and check the numbers.
        results = []
        with open(self.tmp_file, 'r') as csv_handle:
            reader = csv.reader(csv_handle, delimiter=' ')
            for row in reader:
                results.append(row)

        # Make sure it's working properly.
        self.assertTrue(len(results) > 2800)
        self.assertEqual(len(results[0]), 8)
        self.assertEqual(results[0][0], '155.0')
        self.assertEqual(results[10][1], '-28.0')
        self.assertEqual(results[28][2], '-83.0')
        self.assertEqual(results[236][3], '3.0')
        self.assertEqual(results[387][4], '59.0')
        self.assertEqual(results[822][5], '-142.4')
        self.assertEqual(results[1298][6], '-8.1')
        self.assertEqual(results[2150][7], '-39.6')

        return


#===============================================================================
#   Functions:
#===============================================================================

# Main.
if __name__ == "__main__":
    unittest.main()


