""" This module is responsible for the learning of historical data"""
# TODO: Classification. logistic regression. Neural Network.
# TODO: Formulate as outliner detection.

import numpy as np
from strategies import base
from strategies.euler import util

#===============================================================================
#   Classes:
#===============================================================================

class Learner:
    """ Class responsible for learning and predicting rates from
        historical data.
    """

    def __init__(self, instrument):
        """ Initialize the Learner class.

            Args:
                instrument: string. The currency pair. e.g. 'EUR_USD'.

            Returns:
                void.
        """
        self.instrument = instrument
        self.data_file = util.get_clean_data(instrument)
        self.data_mat = base.read_features(self.data_file)
        self.sample_index = 0

        # Checking input read from file.
        assert self.data_mat.shape[1] == 8

        return


    def build_model(self, model, sample_rate, **model_params):
        """ Build a predictive model for predicting the price change of the
            next day. Training and test data both come from self.data_file.

            Args:
                model: sklearn Classifier or Regressor interface.
                    Data from self.data_mat will be used to fit this model.
                sample_rate: float. Proportion of data used for training set.
                model_params: named arguments. Parameters for the model.

            Returns:
                model: sklearn Classifier or Regressor. Trained input model.
        """
        # Update the sample rate and index.
        self.sample_index = int(self.data_mat.shape[0] * sample_rate)

        # Get the training set and values.
        train_set = self.data_mat[:self.sample_index, :-1]
        train_val = self.data_mat[:self.sample_index, -1]

        # Build the model.
        model.set_params(**model_params)
        model.fit(train_set, train_val)

        return model


    def test_model(self, model):
        """ Run a preliminary evaluation of model in terms of its accuracy.

            Args:
                model: sklearn Classifier or Regressor interface.
                    This is the model that will be evaluated.

            Returns:
                test_pred: np.array of dim 1. Prediction results on the test
                    sample from self.sample_index to the end of self.data_mat.
                results: dictionary. Including:
                    ave_diff: Average of prediction error.
                    prop_op: Proportion of predictions in the wrong direction.
        """
        # Get the test set and values.
        test_set = self.data_mat[self.sample_index:, :-1]
        test_val = self.data_mat[self.sample_index:, -1]

        # Make and format the prediction results.
        test_pred = model.predict(test_set)

        # Gather the results.
        results = {}
        results['ave_diff'] = np.fabs(test_pred - test_val).mean()

        # Count the ones that predicted the wrong direction.
        wrongs = (np.multiply(test_pred, test_val) < 0).astype(int)
        results['prop_op'] = wrongs.sum() / wrongs.size

        return test_pred, results


