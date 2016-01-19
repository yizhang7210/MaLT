""" This module provides common resources shared among the project."""

import os
import matplotlib.pyplot as plt

#===============================================================================
#   Constants:
#===============================================================================

#---------------------------------------
# Accounts:
#---------------------------------------

# Account numbers:
TRADE_ACCOUNT = 0
GAME_ACCOUNT = 6483208
GAME_TEST_ACCOUNT = 5561814

# Access tokens.
GAME_TOKEN = "69683ec9c597687072f5793cbba7bfe4-e613b65d8adf1cabeec04cf6d65ab580"
TRADE_TOKEN = ""

#---------------------------------------
# Execution:
#---------------------------------------

# Buy and sell.
BUY = 'buy'
SELL = 'sell'

# Units.
CONSTANT_FACTOR = 200
SQUARE_FACTOR = 0.2
ROOT_FACTOR = 8

# REST end-points.
GAME_URL = "api-fxpractice.oanda.com"
TRADE_URL = "api-fxtrade.oanda.com"

# HTTP request header for game and trade.
GAME_HEADER = {"Content-type": "application/x-www-form-urlencoded", \
    "Authorization" : "Bearer {0}".format(GAME_TOKEN)}

TRADE_HEADER = {}

#---------------------------------------
# Data:
#---------------------------------------

# Currency pairs.
ALL_PAIRS = ['EUR_USD', 'USD_JPY', 'GBP_USD', 'USD_CHF', 'USD_CAD']

# Strategies:
ALL_STRATEGIES = ['Euler']

# Daily candles field names.
CANDLE_FEATURES = ['time', 'openBid', 'highBid', 'lowBid', 'closeBid'] + \
                  ['openAsk', 'highAsk', 'lowAsk', 'closeAsk', 'volume']

# Project Directories.
PROJECT_DIR = os.environ['PYTHONPATH']
DAILY_CANDLES = "{0}/data/store/candles/daily".format(PROJECT_DIR)
DAILY_STRATEGY = "{0}/exec/daily_strategy".format(PROJECT_DIR)

# Start day of historical data.
START_DATE = '2005-01-01'
DATE_LENGTH = len(START_DATE)


#===============================================================================
#   Functions:
#===============================================================================

def get_strategy_loc(instrument):
    """ Obtain the locations of the serialized strategy and its parameters.

        Args:
            instrument: string. The currency pair. e.g. 'EUR_USD'.

        Returns:
            model_loc: string. Path to the serialized model.
            param_loc: string. Path to the serialized strategy parameters.
    """
    model_loc = "{0}/{1}.pkl".format(DAILY_STRATEGY, instrument)
    param_loc = "{0}/{1}.param".format(DAILY_STRATEGY, instrument)

    return model_loc, param_loc


def get_strategy_module(strategy_name):
    """ Obtain the module where the strategy class is defined.

        Args:
            strategy_name: string. Name of the strategy. e.g. 'Euler'.

        Returns:
            module: module variable, where the strategy class is defined.
    """
    module_name = strategy_name.lower()
    package = __import__('strategies' + ('.' + module_name) * 2)
    module = getattr(getattr(package, module_name), module_name)

    return module


def price_to_pip(price, pip_factor):
    """ Numbers are format to 1 decimal places in pips.

        Args:
            price: float. Actual price of instrument.
            pip_factor: int. The multiplier for calculating pip from price.

        Returns:
            pip_string: string. The price in pips with 1 decimal place.
    """
    pip = price * pip_factor
    pip_string = "{0:.1f}".format(pip)

    return pip_string


def list_to_float(lst):
    """ Change the entire list to float.

        Args:
            lst: list of strings.

        Returns:
            floats: ist of floats. The values in floats.
    """
    floats = [float(x) for x in lst]

    return floats


def get_pip_factor(instrument):
    """ Obtain the price to pip multiplier. It's usually 10000, in
        various currency pairs involving JPY, it could be 100.

        Args:
            instrument: string. The currency pair. e.g. 'EUR_USD'.

        Returns:
            factor: int. Either 100 or 10000, depending on the instrument.
    """
    if instrument in ['USD_JPY']:
        factor = 100
    else:
        factor = 10000

    return factor


def plot(vector, name):
    """ Plot the vector and save the picture to the name.

        Args:
            vector: list of floats. The vector to be plotted.
            name: string. Name for the picture to be saved.

        Returns:
            void.
    """
    plt.plot(vector)
    plt.title(name)
    plt.savefig(name)
    plt.close()

    return


def get_raw_data(instrument):
    """ Returns the location of the raw historical daily candle data file.

        Args:
            instrument: string. The currency pair. e.g. 'EUR_USD'.

        Returns:
            path: string. File path to the raw daily candle data file.
    """
    path = '{0}/{1}.csv'.format(DAILY_CANDLES, instrument)

    return path


