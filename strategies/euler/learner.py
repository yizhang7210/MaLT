""" This package is responsible for the learning of historical data"""
# TODO: Next: logistic regression. Next: formulate as classification problem.
#       All small changes are essentially the same, we don't care.
# TODO: Euler with take profit (predicted amount) and stoploss (half predicted
#       amount opposite direction)


from strategies import util
import numpy as np
from sklearn import tree
import common
import csv

class Learner:
    """ Class responsible for learning and prediction rates from
        historical data.
    """
    def __init__(self, instrument):
        """ Initialize the Learner class.

            Args:
                instrument: String. Name of the instrument of interest.

            Returns:
                Void.
        """
        self.instrument = instrument
        self.data_file = '{0}/strategies/euler/store/{1}.csv'. \
                         format(common.PROJECT_DIR, instrument)
        self.test_file = '{0}/data/store/candles/daily/{1}.csv'. \
                         format(common.PROJECT_DIR, instrument)
        self.data_mat = util.read_to_matrix(self.data_file)
        self.sample_rate = 0
        self.sample_index = 0
        self.model = None


    def build_model(self, sample_rate, export_tree=False, **model_params):
        """ Build a CART model for predicting the price change of next day,
            and saves it to self.model. The training and test data sets both
            come from self.data_file.

            Args:
                sample_rate: Float. Proportion of data used for training set.
                export_tree: Boolean. Whether to export the tree of the model.
                model_params: Named arguments. Parameters for the CART model.

            Returns:
                model: A CART model for predicting daily price changes.
        """
        # Update the sample rate and index.
        self.sample_rate = sample_rate
        self.sample_index = int(self.data_mat.shape[0] * sample_rate)

        # Get the training set and values.
        train_set = self.data_mat[:self.sample_index, :-1]
        train_val = self.data_mat[:self.sample_index, -1]

        # Build the model.
        model = tree.DecisionTreeRegressor()
        model.set_params(**model_params)
        model = model.fit(train_set, train_val)

        # Export the model if required.
        if export_tree:
            tree.export_graphviz(model)

        self.model = model


    def test_model(self):
        """ Run a preliminary evaluation of self.model.

            Args:
                Void.

            Returns:
                test_pred: Column matrix. Prediction results on the test sample
                    that is the 1 - self.sample_rate proportion of the data
                    matrix counting from the end.
                result: Dictionary. Including:
                    ave_diff: Average of prediction error.
                    prop_op: Proportion of predictions in the wrong direction.
        """

        # Get the test set and values.
        test_set = self.data_mat[self.sample_index:, :-1]
        test_val = self.data_mat[self.sample_index:, -1]

        # Make and format the prediction results.
        test_pred = self.model.predict(test_set)
        test_pred = test_pred.reshape(test_pred.shape[0], 1)

        # Gather the results.
        results = {}
        results['ave_diff'] = np.fabs(test_pred - test_val).mean()

        # Count the ones that predicted the wrong direction.
        wrongs = (np.multiply(test_pred, test_val) < 0).astype(int)
        results['prop_op'] = wrongs.sum() / wrongs.size

        return test_pred, results


    def dry_run(self, threshold, report_file="dry_run.txt"):
        """ Do a dry run of this strategy on self.test_file as if the strategy
            was put in place. Produce a report on the profitability of this
            strategy over the given period.

            Args:
                threshold: Float. Positive. The strategy will take action if
                    the predicted price change is above threshold. e.g. if
                    predicted price is < -threshold, will sell.
                out_file: String. Name of the output file for the report.
            Returns:
                Void.
        """

        # Obtain prediction results first.
        test_pred, results = self.test_model()

        # Write report title and short results.
        title = "Dry run report for threshold {0}\n\n".format(threshold)
        report = open(report_file, 'w')
        report.write(title)
        report.write("========== Prediction Results ==========\n")
        report.write("Average Prediction error: {0} pips.\n". \
                format(results['ave_diff']))
        report.write("Proportion of wrongly predicted directions: {0}\n". \
                format(results['prop_op']))

        # Time for the dry run results.
        report.write("\n========== Dry Run Results ==========\n")
        # Now go through the actual daily candles and figure out actual PL.
        test_file_handle = open(self.test_file, 'r')

        reader = csv.reader(test_file_handle, delimiter=' ')

        # Skip the title line.
        next(test_file_handle)

        # Initialize some indecies.
        this_line_number = 0
        test_line_number = 0
        total_profit_loss = 0

        # Go through each line in the actual daily candle file.
        for line in reader:

            if this_line_number <= self.sample_index:
                # Skip all lines before sample_index. They are not tested.
                this_line_number += 1
            else:

                # Into the tested region. Get the date first.
                date = line[0]

                # Fetch the predicted and actual price change.
                predicted = test_pred[test_line_number][0]
                actual = self.data_mat[this_line_number - 1, -1]

                # Increment the indices for the loop.
                test_line_number += 1
                this_line_number += 1

                # TODO: have a separate get_units function.
                if predicted > threshold:
                    # BUY:
                    direction = "buy"
                    # Predicted large price increase. Buy.
                    units = int(predicted)

                elif predicted < -threshold:
                    # SELL:
                    direction = "sell"
                    # Predicted large price drop. Sell.
                    units = -int(predicted)
                else:
                    continue

                # Calculate profit/loss.
                p_l = get_profit_loss(line, units, direction)

                # Add to the report.
                row = format_line(date, direction, predicted, actual, p_l)
                report.write(row)

                # Update total profit/loss
                total_profit_loss += p_l

        report.write("Total PL is {0}\n".format(total_profit_loss))
        report.close()
        test_file_handle.close()


def get_profit_loss(line, units, direction):
    """ Calculate profit/loss from the daily candle.

        Args:
            line: List of Strings. Date + OHLC of Bid/Ask + volume.
            units: int. Number of units for trade.
            direction: String. 'buy' or 'sell'

        Returns:
            profit_loss: Float. Profit or loss from buy at open and sell at
                close, or sell at open and buy at close.
    """

    if direction == "buy":
        profit_loss = units - units * float(line[5]) / float(line[4])
    elif direction == "sell":
        profit_loss = units * float(line[1]) / float(line[8]) - units
    else:
        raise RuntimeError("get_profit_loss(): To calculate the profit/loss \
                of an action, the direction needs to be 'buy' or 'sell'")
    return profit_loss

def format_line(date, direction, predicted, actual, p_l):
    """ Format the line of the day for the dry run report.

        Args:
            date: String. Date.
            direction: String. 'buy' or 'sell'
            predicted: Float. Predicted price change.
            actual: Float. Actual price change.
            p_l: Float. Profit or loss of the day.

        Returns:
            row: String. A sentence containing all the information.
    """
    row = "Date: {0}. Action: {1}. Predicted change: {2}.". \
           format(date, direction, predicted)
    row += "Actual change: {0}. Realized PL: {1}.\n".format(actual, p_l)

    return row


def main():
    """Main"""

    for instrument in common.ALL_PAIRS:
        out_file = "store/{0}_dry_run.txt".format(instrument)
        learner = Learner(instrument)
        learner.build_model(0.8)
        learner.dry_run(100, out_file)

# Main.
if __name__ == "__main__":
    main()












