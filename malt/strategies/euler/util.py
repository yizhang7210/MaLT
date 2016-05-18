""" This module is responsible for providing shared constants, functions and
    utilities for strategy Euler, including data formatting, calculation, and
    strategy and model level parameter building.
"""

# External imports
from sklearn import tree

# Internal imports
from malt import common

#===============================================================================
#   Constants:
#===============================================================================

BIG_RISE = 1
BIG_FALL = -1


#===============================================================================
#   Functions:
#===============================================================================

def get_all_models():
    """ Return all predictive models used for strategy Euler.

        Args:
            void.

        Returns:
            all_models: set. A set of bare-bone predictive models.
    """
    all_models = [tree.DecisionTreeRegressor()]

    return all_models


def get_model_params(model):
    """ Get the parameter space for each type of model.

        Args:
            model: sklearn Classifier or Regressor interface.

        Returns:
            params: list of dicts. Each entry a set of parameters for the model.
    """
    if isinstance(model, tree.tree.BaseDecisionTree):
        # Params for tree models.
        params = [{'max_depth': x, 'min_samples_split': y} \
              for x in range(4, 11, 2) \
              for y in range(2, 21, 4)]

    return params


def get_euler_params():
    """ Get the parameter space for strategy Euler.

        Args:
            void.

        Returns:
            params: list of dicts. Each entry a set of parameters for Euler,
            including:
                threshold: positive float. If predicted price change is more
                    than the threshold, the strategy takes action (buy/sell).
                unit_shape: string. Describes the relationship between the
                    number of units and predicted value. One of 'constant',
                    'linear', 'quadratic', or 'root'
                stop_loss: float. Price for stop loss order.
                take_profit: float. Price for take profit order.
                trailing_stop: float. Pips for trailing stop order.
    """
    params = [{'threshold': x, 'unit_shape': shape, 'trailing_stop': 15} \
             for x in [40., 60., 80., 100.]\
             for shape in ['constant', 'linear', 'quadratic', 'root']]

    return params


def get_clean_data(instrument):
    """ Returns the location of the transformed daily candle data file that
        is ready for strategy Euler to run its learning algorithms.

        Args:
            instrument: string. The currency pair. e.g. 'EUR_USD'.

        Returns:
            path: string. File path to the transformed data file.
    """
    path = "{0}/strategies/euler/store/{1}.csv". \
            format(common.PROJECT_DIR, instrument)

    return path


def get_profit_loss(row, units, **controls):
    """ Calculate profit/loss for a single day from the daily candle.

        Args:
            row: list of strings. Should contain: time, openBid, highBid,
                lowBid, closeBid, openAsk, highAsk, lowAsk, closeAsk, volume.
            units: signed int. Number of units for trade.
                Positive for buy and negative for sell.
            controls: named arguments, including:
                take_profit, stop_loss in price and trailing_stop in pips.

        Returns:
            profit_loss: float. Profit or loss from buy at open and sell at
                close, or sell at open and buy at close, or order triggers.
    """
    # Remove 'time' and 'volume' from the row.
    row = common.list_to_float(row[1:-1])

    # TODO: Take profit.
    # Determine if there's a stop loss price.
    if 'stop_loss' in controls:
        stop_loss_price = controls['stop_loss']
    elif 'trailing_stop' in controls:
        stop_loss_price = controls['trailing_stop']
    else:
        stop_loss_price = -1

    # Calculate profit/loss according to units and price.
    if units == 0:
        # No action.
        profit_loss = 0

    elif units > 0:
        # BUY.
        # If stop loss set and lowBid droped below it, it triggers.
        if stop_loss_price > 0 and row[2] < stop_loss_price:
            sold_price = stop_loss_price
        else:
            sold_price = row[3]
        # Now calculate profit/loss.
        profit_loss = units - units * row[4] / sold_price

    else:
        # SELL.
        # If stop loss set and highAsk rose above it, it triggers.
        if stop_loss_price > 0 and row[5] > stop_loss_price:
            bought_price = stop_loss_price
        else:
            bought_price = row[7]
        # Now calculate profit/loss.
        profit_loss = units - units * row[0] / bought_price

    return profit_loss


def get_price_change(row, pip_factor):
    """ If closeBid - openAsk > 0. Can buy. Return value positive.
        If closeAsk - openBid < 0. Can sell. Return value negative.
        Otherwise do nothing. Return 0.

        Args:
            row: list of Strings. A row from data file in /data/store/
            pip_factor: int. The multiplier for calculating pip from price.

        Returns:
            price_change: string. Profitable price change for the day in pips,
                formatted to 1 decimal place.
    """
    row = common.list_to_float(row[1:-1])

    if row[3] - row[4] > 0:
        diff = row[3] - row[4]
    elif row[7] - row[0] < 0:
        diff = row[7] - row[0]
    else:
        diff = 0

    price_change = common.price_to_pip(diff, pip_factor)

    return price_change


def get_strategy_score(balance):
    """ Calculate a score for a strategy if these were the account balances
        for a period of time.

        Args:
            balance: np.array.  Accumulated profit/loss for a period of time.

        Returns:
            score: float. A number representing the profitability of this
                strategy. The higher the better. Right now it's the proportion
                of days where balance is positive. So it's between 0 and 1.
    """
    score = len(balance[balance > 0]) / float(len(balance))

    return score


def format_row(date, units, predicted, actual, profit_loss):
    """ Format the row of the day for pretty printing.

        Args:
            date: string. Date in readable format.
            units: signed int. Number of units for trade.
                Positive for buy. Negative for sell.
            predicted: float. Predicted price change.
            actual: float. Actual price change.
            profit_loss: float. Profit or loss of the day.

        Returns:
            row: string. A sentence containing all the information.
    """
    if units == 0:
        return ""

    if units > 0:
        words = "Bought {0} units".format(units)
    else:
        words = "Sold {0} units".format(-units)

    row = "{0}. {1}. Predicted: {2: >6}  Actual: {3: >6} PL: {4}.\n". \
           format(date, words, predicted, actual, profit_loss)

    return row


