""" This package is responsible for the learning of historical data"""

from strategies import util
import numpy as np
from sklearn import tree
import common

class Learner:
    """ Class responsible for learning and prediction rates from
        historical data.
    """
    def __init__(self, instrument):
        self.instrument = instrument
        self.data_file = 'store/{0}.csv'.format(instrument)
        self.test_file = '{0}/data/store/candles/daily/{1}.csv'. \
                         format(common.PROJECT_DIR, instrument)
        self.data_mat = util.read_to_matrix(self.data_file)

    def build_model(self, sample_rate):
        """ Build the machine learning model for prediction

            Args:
                sample_rate: Float. Proportion of data used for training set.

            Returns:
                model: Anything that has a 'predict' method for prediction.
        """

        # Get number of rows, columns, and training samples.
        train_index = int(self.data_mat.shape[0] * sample_rate)

        # Get the training set and values.
        train_set = self.data_mat[:train_index, :-1]
        train_val = self.data_mat[:train_index, -1]

        # Build the model.
        model = tree.DecisionTreeRegressor(max_depth=4, min_samples_split=10)
        model = model.fit(train_set, train_val)

        return model

    def test_model(self, model, test_rate):
        """ Run a preliminary evaluation of a model.

            Args:
                model: Anthing that has a 'predict' method for prediction.
                test_rate: Float. Proportion of data used for testing.

            Returns:
                result: Dictionary. Including:
                    ave_diff: Average of prediction error.
                    prop_op: Proportion of predictions in the wrong direction.
        """

        # Get the test set and values.
        test_index = int(self.data_mat.shape[0] * (1 - test_rate))
        test_set = self.data_mat[test_index:, :-1]
        test_val = self.data_mat[test_index:, -1]

        # Make and format the prediction results.
        test_pred = model.predict(test_set)
        test_pred = test_pred.reshape(test_pred.shape[0], 1)

        # Obtain the results
        results = {}
        results['ave_diff'] = np.fabs(test_pred - test_val).mean()

        vec = (np.multiply(test_pred, test_val) < 0).astype(int)
        results['prop_op'] = vec.sum()/vec.size

        return results

    def dry_run():
        """ Do a dry run of this strategy on historical data
            and produce a report on how it did.
        """



def main():
    """Main"""

    learner = Learner('USD_CHF')
    mod = learner.build_model(0.8)
    res = learner.test_model(mod, 0.2)
    print(res)

# Main.
if __name__ == "__main__":
    main()













