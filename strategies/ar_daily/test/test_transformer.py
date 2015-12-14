""" This is the test module for the ar_daily strategy module."""

import unittest
import os
import csv
from strategies.ar_daily import transformer

class TestTransformer(unittest.TestCase):
    """ Class for testing transformer."""

    def setUp(self):
        """ Set up temporary files."""
        self.tmp_file = "tmp.csv"

    def tearDown(self):
        """ Delete temporary files."""
        if os.path.isfile(self.tmp_file):
            os.remove(self.tmp_file)

    def test_transformation(self):
        """ Test the data gets transformed and written properly."""
        # Pick the path and transform the data.
        project_dir = os.environ['PYTHONPATH']
        in_file = "{0}/data/store/candles/daily/USD_CHF.csv".format(project_dir)
        transformer.transform(in_file, self.tmp_file, 10000)

        # Read the file and check the numbers.
        results = []
        with open(self.tmp_file, 'r') as csv_handle:
            reader = csv.reader(csv_handle, delimiter=' ')
            for row in reader:
                results.append(row)

        self.assertTrue(len(results) > 3100)
        self.assertEqual(len(results[0]), 8)
        self.assertEqual(results[0][0], '19.0')
        self.assertEqual(results[10][1], '-18.0')
        self.assertEqual(results[28][2], '20.0')
        self.assertEqual(results[236][3], '10.0')
        self.assertEqual(results[387][4], '95.0')
        self.assertEqual(results[1822][5], '-40.0')
        self.assertEqual(results[2618][6], '25.5')
        self.assertEqual(results[3131][7], '-15.2')

# Main.
if __name__ == "__main__":
    unittest.main()





