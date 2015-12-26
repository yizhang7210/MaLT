""" This module is responsible for providing shared constants, functions
and utilities for strategy Euler.
"""

import common
from strategies import util

#===============================================================================
#   Constants:
#===============================================================================

BIG_RISE = 1
BIG_FALL = -1


#===============================================================================
#   Functions:
#===============================================================================

def get_raw_data(instrument):
    """ Returns the location of the raw historical daily candle data file.

        Args:
            instrument: string. Instrument of interest. e.g. EUR_USD.

        Returns:
            path: string. File path to the raw daily candle data file.
    """
    path = '{0}/{1}.csv'.format(common.DAILY_CANDLES, instrument)

    return path


def get_clean_data(instrument):
    """ Returns the location of the transformed daily candle data file that
        is ready for strategy Euler to run its learning algorithms.

        Args:
            instrument: string. Instrument of interest. e.g. EUR_USD.

        Returns:
            path: string. File path to the transformed data file.
    """
    path = "{0}/strategies/euler/store/{1}.csv". \
            format(common.PROJECT_DIR, instrument)

    return path


def get_profit_loss(row, units):
    """ Calculate profit/loss for a single day from the daily candle.

        Args:
            row: list of Strings. Date + OHLC of Bid/Ask + volume.
            units: signed int. Number of units for trade.
                Positive for buy. Negative for sell.

        Returns:
            profit_loss: float. Profit or loss from buy at open and sell at
                close, or sell at open and buy at close.
    """

    if units == 0:
        # No action.
        profit_loss = 0
    elif units > 0:
        # BUY.
        profit_loss = units - units * float(row[5]) / float(row[4])
    else:
        # SELL.
        profit_loss = units - units * float(row[1]) / float(row[8])

    return profit_loss


def get_price_change(row, pip_multiplier):
    """ If closeBid - openAsk > 0. Can buy. Return value positive.
        If closeAsk - openBid < 0. Can sell. Return value negative.
        Otherwise do nothing.

        Args:
            row: list of Strings. A row from data file in store/
            pip_multiplier: int. The multiplier for calculating pip from price.

        Returns:
            float. Profitable price change for the day in pips.
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















