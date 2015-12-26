""" This module is responsible for back testing strategy Euler on historical
    daily candles.
"""

import common
import matplotlib.pyplot as plt
import numpy as np
from sklearn import tree
from strategies import util
from strategies.euler import euler
from strategies.euler import transformer
from strategies.euler.learner import Learner


#===============================================================================
#   Classes:
#===============================================================================

class BackTester():
    """ Class responsible for back testing predictive models in strategy Euler
        on historical daily candles.
    """

    def __init__(self, instrument):
        """ Initialize the BackTester class.

            Args:
                instrument: string. Name of the instrument of interest.

            Returns:
                void.
        """
        self.instrument = instrument
        self.pip_multiplier = util.get_pip_multiplier(instrument)
        self.test_file = euler.get_raw_data(instrument)
        self.test_data = transformer.read_raw_file(self.test_file)


    def export_plot(self, balance, plot_name):
        """ Export the plot of the dry run balance to picture.

            Args:
                balance: list of floats. The running balance to plot.
                plot_name: string. Name for the picture to be saved.

            Returns:
                void.
        """
        plt.plot(balance)
        plt.title(self.instrument)
        plt.savefig(plot_name)
        plt.close()


    def dry_run(self, test_pred, threshold, **kwargs):
        """ Do a dry run of this strategy on self.test_data as if the strategy
            was put in place. Produce a report on the profitability of this
            strategy over the given period.

            Args:
                test_pred: np.vector. Predicted values for data points in the
                    last part of self.test_data.
                threshold: float. Positive. The strategy will take action if
                    the predicted price change is above threshold. e.g. if
                    predicted price is < -threshold, we will sell.
                kwargs: named arguments, including:
                    print_result: boolean. Whether to print dry run report.
                    export_plot: string. Name of the plot to be saved.

            Returns:
                balance: list of float. Overall profit/loss for every day.
        """

        # Write report title.
        report = "\nDry run report for {0} at threshold {1}\n\n". \
                  format(self.instrument, threshold)
        report += ("="*80 + "\n")

        # Initialize the balance.
        test_size = test_pred.size
        balance = np.zeros([test_size,])

        # Now go through the actual daily candles and figure out actual PL.
        test_rows = self.test_data[-test_size:]

        for i in range(len(test_rows)):

            # Fetch the row.
            row = test_rows[i]

            # Get the date first.
            date = row[0]

            # Fetch the predicted and actual price change.
            predicted = test_pred[i]
            actual = euler.get_price_change(row, self.pip_multiplier)

            # Figure out the action we take and the units.
            units = get_units(predicted, threshold)

            # Calculate profit/loss for this day.
            p_l = euler.get_profit_loss(row, units)

            # Update daily profit/loss
            balance[i] = balance[i - 1] + p_l

            # Add to the report.
            report += euler.format_row(date, units, predicted, actual, p_l)

        # Add final total profit/loss to the report.
        report += "Total profit/loss: {0}".format(balance[-1])

        # Export the graphs if asked.
        if 'export_plot' in kwargs:
            # Do some plots.
            self.export_plot(balance, kwargs['export_plot'])

        # Print the report if asked.
        if 'print_result' in kwargs and kwargs['print_result']:
            print(report)

        return balance


#===============================================================================
#   Functions:
#===============================================================================

def get_units(predicted, threshold):
    """ Return the units to buy/sell given the predicted price change for
        a particular day.

        Args:
            predicted: float. Predicted price change for the day in pips.
            threshold: float. A threshold below which no action is taken.

        Returns:
            units: signed int. Number of units to buy or sell at open.
                Positive for buy. Negative for sell.
    """
    if abs(predicted) < threshold:
        return 0
    else:
        return int(predicted)


def tune_model(model, instrument, model_param_space):
    """ Given the model and the instrument, attempt to find the best set of
        parameters for prediction.

        Args:
            model: sklearn Classifier or Regressor interface.
            instrument: string. Name of the instrument of interest.
            model_param_space: list of dictionaries. Each entry is a set of
                parameters for the model. Will go through them and find the
                best params in terms of profitability.

        Returns:
            int. Index in the model_param_space that when used, gave the highest
                lowest_balance during the run.
    """
    # Initialize the learner and tester first.
    learner = Learner(instrument)
    tester = BackTester(instrument)

    # Keep a score of each set of parameters.
    param_score = []

    # Go through each set of parameters and score them.
    for param_num in range(len(model_param_space)):

        # Fetch the params and threshold.
        model_param = model_param_space[param_num]
        threshold = model_param.pop('threshold')

        # Initialize average balance and lowest balance.
        ave_balance = []
        lowest_balance = float('inf')

        # Do a number of runs just to be careful.
        for _ in range(10):

            # Build the model and do the dry run.
            model = learner.build_model(model, 0.9, **model_param)
            pred, _ = learner.test_model(model)

            balance = tester.dry_run(pred, threshold)
            ave_balance.append(balance)

            # Update the lowest balance point of the dry run.
            lowest_balance = min(min(balance), lowest_balance)

        param_score.append(lowest_balance)

        # Take the row average and plot to see how the strategy performs.
        plot_name = '{0}_param_{1}'.format(instrument, param_num)
        ave_balance = np.array(ave_balance).mean(axis=0)
        tester.export_plot(ave_balance, plot_name)

    # Return the index where the lowest_balance is the highest.
    return np.argmax(param_score)


def main():
    """Main"""

    model = tree.DecisionTreeRegressor()

    for instrument in common.ALL_PAIRS:
        all_params = util.build_tree_params()
        best_model_index = tune_model(model, instrument, all_params)
        print(instrument)
        print(all_params[best_model_index])


# Main.
if __name__ == "__main__":
    main()








