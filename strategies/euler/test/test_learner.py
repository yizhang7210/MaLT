""" This is the test module for learner.py."""

import common
import unittest
from sklearn import tree
from strategies import base
from strategies.euler.learner import Learner

#===============================================================================
# Classes:
#===============================================================================

class TestLearner(unittest.TestCase):
    """ Class for testing learner."""

    def setUp(self):
        """ Set up temporary files."""
        test_dir = common.PROJECT_DIR + '/strategies/euler/test'
        self.tmp_file = "{0}/GBP_USD_test_clean.csv".format(test_dir)

        return


    def tearDown(self):
        """ Delete temporary files."""
        pass


    def test_leaner_tree_regressor(self):
        """ Test the learner builds and tests a tree regressor properly."""
        # Initialize model with fixed random state.
        model = tree.DecisionTreeRegressor(random_state=888)

        # Initialize learner and force load test data.
        learner = Learner("GBP_USD")
        learner.data_mat = base.read_features(self.tmp_file)

        # Build model and test preliminary results.
        learner.build_model(model, 0.78)
        pred, result = learner.test_model(model)

        # Test the results.
        self.assertEqual(pred.size, 628)
        self.assertEqual(pred[0], -160.2)
        self.assertEqual(pred[200], -31.0)
        self.assertEqual(pred[-30], -53.6)
        self.assertEqual(len(result), 2)
        self.assertEqual(round(result['ave_diff'], 4), 88.3980)
        self.assertEqual(round(result['prop_op'], 4), 0.4341)

        return


#===============================================================================
#   Functions:
#===============================================================================

# Main.
if __name__ == "__main__":
    unittest.main()


