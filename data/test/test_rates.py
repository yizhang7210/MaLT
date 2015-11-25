""" This is the test module for the data component.
"""

import unittest
import os
import csv
from data import rates

class TestDailyCandles(unittest.TestCase):
    """ Class for testing daily candles
    """

    def setUp(self):
        """ Set up temporary files
        """
        self.tmp_file = "tmp.csv"

    def tearDown(self):
        """ Delete temporary files
        """
        if os.path.isfile(self.tmp_file):
            os.remove(self.tmp_file)

    def test_get_candles(self):
        """ Test obtaining daily candles correctly
        """
        candles = rates.get_daily_candles("EUR_USD", "2015-11-07", "2015-11-11")
        self.assertEqual(len(candles), 3)
        self.assertEqual(candles[0]['lowBid'], 1.07186)
        self.assertEqual(candles[1]['highAsk'], 1.07649)
        self.assertEqual(candles[2]['volume'], 26025)

    def test_write_candles(self):
        """ Test writing candles to file
        """
        # Get the candles.
        candles = rates.get_daily_candles("USD_JPY", "2013-11-08", "2013-11-20")

        # Write the candles to file.
        rates.write_candles_to_csv(candles, self.tmp_file)

        # Read the file and check the results.
        results = []
        with open(self.tmp_file, 'r') as csvhandle:
            reader = csv.reader(csvhandle, delimiter=' ')
            for row in reader:
                results.append(row)

        self.assertEqual(len(results), 10)
        self.assertEqual(len(results[0]), 10)
        self.assertTrue('time' in results[0])
        self.assertTrue('99.115' in results[5])
        self.assertTrue('2013-11-19' in results[9])

# Main.
if __name__ == "__main__":
    unittest.main()















