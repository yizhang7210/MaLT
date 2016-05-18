""" This is the test module for util.py."""

# External imports
import numpy as np
import unittest
from sklearn import tree

# Internal imports
from malt.strategies.euler import util

#===============================================================================
# Classes:
#===============================================================================

class TestUtil(unittest.TestCase):
    """ Class for testing util."""

    def setUp(self):
        """ Set up temporary files."""
        pass


    def tearDown(self):
        """ Delete temporary files."""
        pass


    def test_params(self):
        """ Make sure the parameter spaces are correct."""
        # First up, a tree model.
        tree_model = tree.DecisionTreeClassifier()
        model_params = util.get_model_params(tree_model)
        self.assertEqual(len(model_params), 20)
        self.assertEqual(model_params[0]['max_depth'], 4)
        self.assertEqual(model_params[-3]['min_samples_split'], 10)

        # Now params for strategy Euler.
        strategy_params = util.get_euler_params()
        self.assertEqual(len(strategy_params), 16)
        self.assertEqual(strategy_params[3]['unit_shape'], 'root')
        self.assertEqual(strategy_params[-2]['threshold'], 100.0)

        return


    def test_get_price_change(self):
        """ Make sure the price change is calculated correctly."""
        # Copied a row from EUR_USD raw file.
        row = ['2006-07-20', '1.26278', '1.26953', '1.26234', '1.269'] + \
              ['1.26293', '1.27015', '1.26249', '1.27', '13111']
        price_change = util.get_price_change(row, 10000)

        # Check the calculation.
        self.assertEqual(price_change, '60.7')

        return


    def test_strategy_score(self):
        """ Make sure the strategy score is calculated properly."""
        # Make up some arbitrary balance vector.
        balance = [0, 4.5, 8, -19, -8, 4, 5, -1, 4, 5, 33, 2, 0, 0, 3, 3, 3]
        balance = np.array(balance)
        score = util.get_strategy_score(balance)

        # Check the score.
        self.assertEqual(score, 11.0/17)

        return


#===============================================================================
#   Functions:
#===============================================================================

# Main.
if __name__ == "__main__":
    unittest.main()


