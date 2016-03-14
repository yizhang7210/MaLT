""" This module is responsible for making daily trades. It should be scheduled
    to run everyday at just before 17:00 America/New York time.
"""

import common
logger = common.get_logger(__name__)
import datetime
import json
import time
from data import rates
from exec.executor import Executor
from sklearn.externals import joblib

#===============================================================================
#   Functions:
#===============================================================================

def get_yesterdays_candle(instrument):
    """ Get the (supposedly complete) candle of yesterday just as today begins.

        Args:
            instrument: string. The currency pair. e.g. 'EUR_USD'.

        Returns:
            candle: dict. Standard candle with time, bid/ask OHLC and volume.
    """
    # Get start/end dates.
    start_date = str(datetime.date.today() - datetime.timedelta(3))
    end_date = str(datetime.date.today())

    # Intend to run this script at day's open (e.g. 17:01) so the last candle
    # is yesterday's candle.
    candle = rates.get_daily_candles(instrument, start_date, end_date)[-1]

    return candle


def run_at_day_close(executor):
    """ Run the operations at day's close. Close all open trades.

        Args:
            executor: exec.Executor. The object for executing trades.

        Returns:
            void.
    """
    executor.close_all_trades()

    return


def run_at_day_open(executor, instrument):
    """ Run the operations at day's open. Gather yesterday's prices, predict
        today's price changes and take appropriate actions.

        Args:
            executor: exec.Executor. The object for executing trades.
            instrument: string. The currency pair. e.g. 'EUR_USD'.

        Returns:
            void.
    """
    # Log.
    logger.info("Daily run: On %s.", instrument)

    # Get yesterday's candle first.
    yesterdays_candle = get_yesterdays_candle(instrument)

    # Load the model strategy parameters.
    model_loc, param_loc = common.get_strategy_loc(instrument)
    model = joblib.load(model_loc)
    strategy_params = json.load(open(param_loc, 'r'))
    logger.info("Strategy: %s.", str(strategy_params))

    # Instantiate the right strategy object from name.
    name = strategy_params['name']
    module = common.get_strategy_module(name)
    strategy = getattr(module, name)(instrument)

    # Set the parameters.
    strategy.set_params(**strategy_params)
    strategy.model = model
    logger.info("Model: %s.", str(model))

    # Execute.
    strategy.execute(executor, yesterdays_candle)

    return


def main():
    """ Main in daily_run. Run daily trading strategies on each instrument.

        Args:
            void.

        Returns:
            void.
    """
    # Log enter.
    logger.info("Daily run: Starting.")

    # Initialize executor and check today's weekday.
    executor = Executor(common.GAME_STAGING_ACCOUNT)
    weekday = datetime.date.today().weekday()

    # Need to run daily close on Monday - Friday.
    if weekday in [0, 1, 2, 3, 4]:
        # TODO: Report PL from yesterday.
        run_at_day_close(executor)

    # Sleep 60 seconds until the market opens for the next day.
    time.sleep(60)

    # Need to run daily open on Sunday - Thursday.
    if weekday in [6, 0, 1, 2, 3]:
        for instrument in common.ALL_PAIRS:
            run_at_day_open(executor, instrument)

    # Log exit.
    logger.info("Daily run: Done.")

    return


# Main.
if __name__ == "__main__":
    main()


