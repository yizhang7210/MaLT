""" This is the malt.common module.
    This module provides common resources shared among the whole project.
"""

# External imports
import datetime
import json
import logging
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from logging.handlers import TimedRotatingFileHandler

#===============================================================================
#   Constants:
#===============================================================================

#---------------------------------------
# Data:
#---------------------------------------

# Currency pairs.
ALL_PAIRS = ['EUR_USD', 'USD_JPY', 'GBP_USD', 'USD_CHF', 'USD_CAD']

# Strategies.
ALL_STRATEGIES = ['Euler']

# Daily candles field names.
CANDLE_FEATURES = ['time', 'openBid', 'highBid', 'lowBid', 'closeBid'] + \
                  ['openAsk', 'highAsk', 'lowAsk', 'closeAsk', 'volume']

# Project Directories.
PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
DAILY_CANDLES = "{0}/data/store/candles/daily".format(PROJECT_DIR)
DAILY_STRATEGY = "{0}/exec/daily_strategy".format(PROJECT_DIR)

# Start day of historical data.
START_DATE = '2005-01-01'
DATE_LENGTH = len(START_DATE)

#---------------------------------------
# Accounts:
#---------------------------------------

# Account Details.
ACCOUNT_INFO_FILE = "{0}/../account.info".format(PROJECT_DIR)
ACCOUNT_INFO = json.load(open(ACCOUNT_INFO_FILE, 'r'))

# Account numbers.
TRADE_ACCOUNT = ACCOUNT_INFO.get('Account-Trade')
GAME_ACCOUNT = ACCOUNT_INFO.get('Account-Game')
GAME_DEV_ACCOUNT = ACCOUNT_INFO.get('Account-Game-Dev')
GAME_STAGING_ACCOUNT = ACCOUNT_INFO.get('Account-Game-Staging')

# Access tokens.
GAME_TOKEN = ACCOUNT_INFO.get('Token-Game')
TRADE_TOKEN = ACCOUNT_INFO.get('Token-Trade')

#---------------------------------------
# Execution:
#---------------------------------------

# Buy and sell.
BUY = 'buy'
SELL = 'sell'

# Units.
# Unit shapes.
UNIT_CONSTANT = 'CONSTANT'
UNIT_LINEAR = 'LINEAR'
UNIT_SQUARE = 'SQUARE'
UNIT_LOG = 'LOGARITHM'

# Unit multiplicative factors.
# The number of units should be equal when the predicted price change is 200.
CONSTANT_FACTOR = 200
LINEAR_FACTOR = 1
SQUARE_FACTOR = 0.05   # 1/200
LOG_FACTOR = 37.75     # 200/log(200)
MAX_UNITS = 500

# REST end-points.
GAME_URL = "api-fxpractice.oanda.com"
TRADE_URL = "api-fxtrade.oanda.com"

# HTTP request header for game and trade.
GAME_HEADER = {"Content-type": "application/x-www-form-urlencoded", \
    "Authorization" : "Bearer {0}".format(GAME_TOKEN)}

TRADE_HEADER = {}

# File log location.
LOG_FILE = "{0}/../logs/daily.log".format(PROJECT_DIR)


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
    malt = __import__('malt.strategies' + ('.' + module_name) * 2)
    strategies = getattr(malt, 'strategies')
    strategy_module = getattr(getattr(strategies, module_name), module_name)

    return strategy_module


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


def get_logger(name):
    """ Get the logger for logging events.

        Args:
            name: string. Name of the logger, should be the respective python
                module.

        Returns:
            logger: logger. A logger ready for use.
    """
    # Get the logger.
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # The handler. Create new log file every Sunday at 16:00.
    time = datetime.time(16, 0, 0)
    handler = TimedRotatingFileHandler(LOG_FILE, when='W6', atTime=time)
    handler.setLevel(logging.INFO)

    # The formatter.
    log_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_string)

    # Set the formatter and handler.
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


