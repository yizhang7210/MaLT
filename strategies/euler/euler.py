""" This module is responsible for providing shared constants, functions
and utilities for strategy Euler.
"""

import common
from strategies import util

#====================================================================
#   Constants:
#====================================================================

BIG_RISE = 1
BIG_FALL = -1


#====================================================================
#   Functions:
#====================================================================

def get_raw_data(instrument):
    """ Returns the location of the raw historical daily candle data file.

        Args:
            instrument: String. Instrument of interest. e.g. EUR_USD.

        Returns:
            path: String. File path to the raw daily candle data file.
    """
    path = '{0}/{1}.csv'.format(common.DAILY_CANDLES, instrument)

    return path


def get_clean_data(instrument):
    """ Returns the location of the transformed daily candle data file that
        is ready for strategy Euler to run its learning algorithms.

        Args:
            instrument: String. Instrument of interest. e.g. EUR_USD.

        Returns:
            path: String. File path to the transformed data file.
    """
    path = "{0}/strategies/euler/store/{1}.csv". \
            format(common.PROJECT_DIR, instrument)

    return path


def get_profit_loss(row, units, direction):
    """ Calculate profit/loss for a single day from the daily candle.

        Args:
            row: List of Strings. Date + OHLC of Bid/Ask + volume.
            units: int. Number of units for trade.
            direction: String. 'buy' or 'sell'

        Returns:
            profit_loss: Float. Profit or loss from buy at open and sell at
                close, or sell at open and buy at close.
    """

    if direction == common.BUY:
        profit_loss = units - units * float(row[5]) / float(row[4])
    elif direction == common.SELL:
        profit_loss = units * float(row[1]) / float(row[8]) - units
    else:
        raise RuntimeError("get_profit_loss(): To calculate the profit/loss \
                of an action, the direction needs to be 'buy' or 'sell'")
    return profit_loss


def get_price_change(row, pip_multiplier):
    """ If closeBid - openAsk > 0. Can buy. Return value positive.
        If closeAsk - openBid < 0. Can sell. Return value negative.
        Otherwise do nothing.

        Args:
            row: List of Strings. A row from data file in store/
            pip_multiplier: int. The multiplier for calculating pip from price.

        Returns:
            Profitable price change for the day in pips.
    """
    # TODO: use dictionary instead of indices.
    row = util.list_to_float(row[1:-1])
    if row[3] - row[4] > 0:
        diff = row[3] - row[4]
    elif row[7] - row[0] < 0:
        diff = row[7] - row[0]
    else:
        diff = 0

    return util.price_to_pip(diff, pip_multiplier)


def format_row(date, direction, predicted, actual, profit_loss):
    """ Format the row of the day for pretty printing.

        Args:
            date: String. Date in readable format.
            direction: String. 'buy' or 'sell'
            predicted: Float. Predicted price change.
            actual: Float. Actual price change.
            profit_loss: Float. Profit or loss of the day.

        Returns:
            row: String. A sentence containing all the information.
    """
    row = "{0}. {1: <4} Predicted: {2: >6}  Actual: {3: >6} PL: {4}.\n". \
           format(date, direction, predicted, actual, profit_loss)

    return row
