""" This is the malt.strategies.euler.euler module.
    This module is responsible for defining the strategy class Euler.
"""

# External imports
import json
import math
import numpy as np
from sklearn.externals import joblib

# Internal imports
from malt import common
logger = common.get_logger(__name__)
from malt.strategies.base import BaseStrategy
from malt.strategies.euler import transformer, util
from malt.strategies.euler.learner import Learner

#===============================================================================
#   Classes:
#===============================================================================

class Euler(BaseStrategy):
    """ The strategy class Euler. It attempts to predict daily price change
        from open to close according to previous day's candle.
    """

    # All predictive models used for strategy Euler.
    all_models = util.get_all_models()

    def __init__(self, instrument):
        """ Initialize the strategy class Euler.

            Args:
                instrument: string. The currency pair. e.g. 'EUR_USD'.

            Returns:
                void.
        """
        super(Euler, self).__init__(instrument)

        # Initialize learner and model.
        self.learner = Learner(instrument)
        self.model = None

        # Read in the raw data file for testing.
        test_file = common.get_raw_data(instrument)
        self.test_data = transformer.read_raw_file(test_file)

        return


    def set_params(self, **params):
        """ Set parameters for strategy Euler.

            Args:
                params: named parameters for strategy Euler, including:
                    threshold: positive float. Threshold for the strategy to
                        take action (either buy or sell).
                    unit_shape: string. Describes the relationship between the
                        number of units and predicted value. One of 'constant',
                        'linear', 'quadratic', or 'root'

            Returns:
                void.
        """
        if 'name' in params:
            assert params['name'] == 'Euler'

        params['name'] = 'Euler'
        self.params = params

        return


    def parse_controls(self):
        """ Determine the SL/TP/TS orders for trade from parameters.

            Args:
                void.

            Returns:
                controls: dict. Including take_profit, stop_loss (in price) and
                    trailing_stop (in pips).
        """
        controls = {}
        if 'stop_loss' in self.params:
            controls['stop_loss'] = self.params['stop_loss']

        if 'take_profit' in self.params:
            controls['take_profit'] = self.params['take_profit']

        if 'trailing_stop' in self.params:
            controls['trailing_stop'] = self.params['trailing_stop']

        return controls


    def parse_units(self, pred):
        """ Determine the number of units for trade from parameters.

            Args:
                pred: float. Predicted change in price.

            Returns:
                units: signed int. Number of units for trade.
                    Positive for buy, negative for sell.
        """
        # Get the parameters first.
        unit_shape = self.params['unit_shape']
        threshold = self.params['threshold']

        # Take no action if predicted price change under threshold.
        if pred > threshold:
            sign = 1
        elif pred < -threshold:
            sign = -1
        else:
            return 0

        # Parse different ways of determining units.
        if unit_shape == 'constant':
            # Constant number of units.
            units = common.CONSTANT_FACTOR
        elif unit_shape == 'linear':
            # Units linear in predicted change.
            units = abs(int(pred))
        elif unit_shape == 'quadratic':
            # Units quadratic in predicted change.
            units = int(pred ** 2 * common.SQUARE_FACTOR)
        elif unit_shape == 'root':
            # Units proportional to square root of predicted change.
            units = int(math.sqrt(abs(pred)) * common.ROOT_FACTOR)
        else:
            logger.warn("euler.parse_units(): invalid unit shape.")
            return 0

        units = units * sign

        return units


    def execute(self, executor, candle):
        """ Execute the strategy at day's open.

            Args:
                executor: exec.Executor. The object for executing trades.
                candle: dict. Yesterday's daily candle.

            Returns:
                void.
        """
        # TODO: Report failure.
        # Build and format the features first.
        features = transformer.candle_to_features(candle, self.pip_factor)
        features = np.asarray(features).reshape(1, -1)

        # Making and logging the prediction.
        pred = self.model.predict(features)
        logger.info("Euler: Predicted price change for %s is %.2f.", \
                self.instrument, float(pred))

        # Parse the parameters.
        controls = self.parse_controls()
        units = self.parse_units(pred)

        # Make the decision.
        executor.make_trade(self.instrument, units, **controls)

        return


    def dry_run(self, pred, **kwargs):
        """ Do a dry run of strategy Euler as if the strategy was put in place.
            Return the day-to-day balance during the run, and produce a report
            on the profitability of this strategy over the given period.

            Args:
                pred: np.vector. Predicted daily price changes for days in the
                    last part of the test data.
                kwargs: named arguments, including:
                    print_result: boolean. Whether to print dry run report.
                    export_plot: string. Name of the plot to be saved.

            Returns:
                balance: np.array.  Accumulated profit/loss of every day.
        """
        # Write report title.
        report = "\nDry run report: {0}\n\n".format(self.instrument)
        report += str(self.params) + '\n'
        report += '=' * 80 + '\n'

        # Initialize the balance.
        test_size = pred.size
        balance = np.zeros_like(pred)

        # Now go through the actual daily candles and figure out actual PL.
        data = self.test_data[-test_size:]

        for i in range(len(data)):

            # Fetch the row.
            row = data[i]

            # Fetch the predicted and actual price change.
            predicted = pred[i]
            actual = util.get_price_change(row, self.pip_factor)

            # Figure out the action we take and the units.
            units = self.parse_units(predicted)
            controls = self.parse_controls()

            # Calculate profit/loss for this day.
            p_l = util.get_profit_loss(row, units, **controls)

            # Update daily profit/loss
            balance[i] = balance[i - 1] + p_l

            # Add to the report. row[0] is date.
            report += util.format_row(row[0], units, predicted, actual, p_l)

        # Add final total profit/loss to the report.
        report += "Total profit/loss: {0}".format(balance[-1])

        # Export the graphs if asked.
        if 'export_plot' in kwargs:
            # Do some plots.
            common.plot(balance, kwargs['export_plot'])

        # Print the report if asked.
        if 'print_result' in kwargs and kwargs['print_result']:
            print(report)

        return balance


    def get_best(self):
        """ Produce a best instance of this strategy.

            Args:
                void.

            Returns:
                self: Euler instance. With the params and model having the
                    highest score among all combinations.
        """
        # Log enter.
        logger.info("Euler: Selecting best for %s.", self.instrument)

        # Initialize the scores array and strategy parameters.
        scores = []
        strategy_params = util.get_euler_params()

        # TODO: Do more than 1 run.
        # Run for all predictive models.
        counter = 0
        for model in self.all_models:
            scores_row = []
            model_params = util.get_model_params(model)

            # Try different model parameters.
            for model_param in model_params:
                scores_col = []
                model = self.learner.build_model(model, 0.9, **model_param)
                pred, _ = self.learner.test_model(model)

                # And different strategy parameters, e.g. threshold.
                for strategy_param in strategy_params:
                    self.set_params(**strategy_param)

                    # Do the dry run.
                    plot_name = '{0}_{1}.png'.format(self.instrument, counter)
                    balance = self.dry_run(pred, export_plot=plot_name)

                    # Determine the quality of the params via score.
                    scores_col.append(util.get_strategy_score(balance))
                    counter += 1

                scores_row.append(scores_col)

            scores.append(scores_row)

        # Get the best and set the parameters to the best.
        best = np.unravel_index(np.argmax(scores), np.array(scores).shape)

        model = self.all_models[best[0]]
        model_param = util.get_model_params(model)[best[1]]
        model = self.learner.build_model(model, 1, **model_param)

        logger.info("Best score is: %s.", str(np.array(scores)[best]))
        self.set_params(**strategy_params[best[2]])
        self.model = model

        return self


    def serialize(self):
        """ Serialize this strategy to the designated location.

            Args:
                void.

            Returns:
                void.
        """
        # Get the designated locations.
        model_loc, param_loc = common.get_strategy_loc(self.instrument)

        # Dump the data.
        joblib.dump(self.model, model_loc)
        json.dump(self.params, open(param_loc, 'w'))

        return


#===============================================================================
#   Functions:
#===============================================================================

def main():
    """ Main in selecting and serializing the best Euler strategy."""
    for instrument in common.ALL_PAIRS:
        strategy = Euler(instrument)
        strategy = strategy.get_best()
        strategy.serialize()

# Main.
if __name__ == "__main__":
    main()


