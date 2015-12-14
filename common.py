""" This module provides common resources shared among modules
    in the Data component.
"""

import os

# REST end-points.
GAME_URL = "api-fxpractice.oanda.com"
TRADE_URL = "api-fxtrade.oanda.com"

# Access tokens.
GAME_TOKEN = "69683ec9c597687072f5793cbba7bfe4-e613b65d8adf1cabeec04cf6d65ab580"
TRADE_TOKEN = ""

# Currency pairs.
ALL_PAIRS = ['EUR_USD', 'USD_JPY', 'GBP_USD', 'USD_CHF', 'USD_CAD']

# Project Directory.
PROJECT_DIR = os.environ['PYTHONPATH']

# Start day of historical data.
START_DATE = '2005-01-01'
