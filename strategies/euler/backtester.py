""" This module is responsible for back testing strategy Euler on historical
    daily candles.
"""

import common
import matplotlib.pyplot as plot
import numpy as np
from sklearn import tree
from strategies import util
from strategies.euler import euler
from strategies.euler import transformer
from strategies.euler.learner import Learner


#====================================================================
#   Classes:
#====================================================================

class BackTester():
    """ Class responsible for back testing predictive models in strategy Euler
        on historical daily candles.
    """

    def __init__(self, instrument):
        """ Initialize the BackTester class.

            Args:
                instrument: String. Name of the instrument of interest.

            Returns:
                void.
        """
        self.instrument = instrument
        self.pip_multiplier = util.get_pip_multiplier(instrument)
        self.test_file = euler.get_raw_data(instrument)
        self.test_data = transformer.read_raw_file(self.test_file)


    def dry_run(self, test_pred, threshold):
        """ Do a dry run of this strategy on self.test_data as if the strategy
            was put in place. Produce a report on the profitability of this
            strategy over the given period.

            Args:
                test_pred: np.vector. Predicted values for data points in the
                    last part of self.test_data.
                threshold: Float. Positive. The strategy will take action if
                    the predicted price change is above threshold. e.g. if
                    predicted price is < -threshold, we will sell.
            Returns:
                balance: List of Float. Overall profit/loss for every day.
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
            if predicted > threshold:
                direction = common.BUY
                units = get_units(predicted, threshold)
            elif predicted < -threshold:
                direction = common.SELL
                units = get_units(predicted, threshold)
            else:
                balance[i] = balance[i - 1]
                continue

            # Calculate profit/loss for this day.
            p_l = euler.get_profit_loss(row, units, direction)

            # Update daily profit/loss
            balance[i] = balance[i - 1] + p_l

            # Add to the report.
            report += euler.format_row(date, direction, predicted, actual, p_l)

        # Do some plots.
        plot.plot(balance)
        plot.savefig(self.instrument)
        plot.close()

        report += "Total profit/loss: {0}".format(balance[-1])
        print(report)

        return balance


#====================================================================
#   Functions:
#====================================================================

def get_units(predicted, threshold):
    """ Return the units to buy/sell given the predicted price change for
        a particular day.

        Args:
            predicted: Float. Predicted price change for the day in pips.
            threshold: Float. A threshold below which no action is taken.

        Returns:
            units: int >= 0. Number of units to buy or sell at open.
    """
    if abs(predicted) < threshold:
        return 0
    else:
        return abs(int(predicted))


def main():
    """Main"""

    for instrument in common.ALL_PAIRS:
        model = tree.DecisionTreeRegressor()
        learner = Learner(instrument)
        learner.build_model(model, 0.8)
        pred, result = learner.test_model(model)
        print(result)
        tester = BackTester(instrument)
        tester.dry_run(pred, 100)

# Main.
if __name__ == "__main__":
    main()








