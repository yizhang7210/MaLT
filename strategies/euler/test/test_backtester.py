""" This is the test module for backtester.py"""

import unittest
from sklearn import tree
from strategies import util
from strategies.euler import transformer
from strategies.euler.backtester import BackTester
from strategies.euler.learner import Learner

class TestBackTester(unittest.TestCase):
    """ Class for testing backtester."""

    def setUp(self):
        """ Set up temporary files."""
        self.tmp_raw_file = "GBP_USD_test_raw.csv"
        self.tmp_clean_file = "GBP_USD_test_clean.csv"


    def tearDown(self):
        """ Delete temporary files."""


    def test_backtester(self):
        """ Test the backtester tests a model on historical data properly"""
        # Initialize model with fixed random state.
        model = tree.DecisionTreeRegressor(random_state=888)

        # Initialize learner and force load test data.
        learner = Learner("GBP_USD")
        learner.data_mat = util.read_to_matrix(self.tmp_clean_file)

        # Build model and test preliminary results.
        learner.build_model(model, 0.78)
        pred, _ = learner.test_model(model)

        # Initialize backtester and force load test data.
        tester = BackTester("GBP_USD")
        tester.test_data = transformer.read_raw_file(self.tmp_raw_file)
        balance = tester.dry_run(pred, 85, print_result=False)

        # Test the results.
        self.assertEqual(balance.size, 628)
        self.assertEqual(round(balance[0], 4), -0.1965)
        self.assertEqual(round(balance[210], 4), 0.3467)
        self.assertEqual(round(balance[-143], 4), -19.6579)
        self.assertEqual(round(balance[-30], 4), -20.7953)
        self.assertEqual(round(sum(balance), 4), -4088.2712)


# Main.
if __name__ == "__main__":
    unittest.main()












