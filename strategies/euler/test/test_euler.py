""" This is the test module for euler.py."""

import common
import unittest
from sklearn import tree
from strategies import base
from strategies.euler import euler, transformer
from strategies.euler.learner import Learner

#===============================================================================
# Classes:
#===============================================================================

class TestEuler(unittest.TestCase):
    """ Class for testing euler."""

    def setUp(self):
        """ Set up temporary files."""
        test_dir = common.PROJECT_DIR + '/strategies/euler/test'
        self.tmp_raw_file = "{0}/GBP_USD_test_raw.csv".format(test_dir)
        self.tmp_clean_file = "{0}/GBP_USD_test_clean.csv".format(test_dir)

        return


    def tearDown(self):
        """ Delete temporary files."""
        pass


    def test_dry_run(self):
        """ Test dry run in euler. Check that it tests a model on historical
            data properly.
        """
        # Initialize model with fixed random state.
        model = tree.DecisionTreeRegressor(random_state=888)

        # Initialize learner and force load test data.
        learner = Learner("GBP_USD")
        learner.data_mat = base.read_features(self.tmp_clean_file)

        # Build model and test preliminary results.
        learner.build_model(model, 0.78)
        pred, _ = learner.test_model(model)

        # Initialize Euler and force load test data.
        strategy = euler.Euler("GBP_USD")
        strategy.set_params(unit_shape='linear', threshold=85)
        strategy.test_data = transformer.read_raw_file(self.tmp_raw_file)
        balance = strategy.dry_run(pred)

        # Test the results.
        self.assertEqual(balance.size, 628)
        self.assertEqual(round(balance[0], 4), -0.1965)
        self.assertEqual(round(balance[210], 4), 0.3467)
        self.assertEqual(round(balance[-143], 4), -19.6579)
        self.assertEqual(round(balance[-30], 4), -20.7953)
        self.assertEqual(round(sum(balance), 4), -4088.2712)

        return


#===============================================================================
#   Functions:
#===============================================================================

# Main.
if __name__ == "__main__":
    unittest.main()


