""" This is the malt.exec.daily_train module.
    This module is responsible for updating data, re-training models as well as
    selecting the best strategy during the day. It should be scheduled to run
    everyday at any time after 17:00. Currently it runs at 17:10.
"""

# External imports
import datetime

# Internal imports
from malt import common
logger = common.get_logger(__name__)
from malt.data import rates

#===============================================================================
#   Functions:
#===============================================================================

def run(strategy_name):
    """ Run transformation and model seletion for each strategy.

        Args:
            strategy_name: string. Name of the strategy. e.g. 'Euler'.

        Returns:
            void.
    """
    # Find the transformer and the strategy module.
    module_name = strategy_name.lower()

    # The transformer.
    malt = __import__('malt.strategies.' + module_name + '.transformer')
    strategies = getattr(malt, 'strategies')
    transformer = getattr(getattr(strategies, module_name), 'transformer')

    # The strategy module.
    strategy_module = common.get_strategy_module(strategy_name)

    # Run their respective main functions.
    transformer.main()
    strategy_module.main()

    return


def main():
    """ Main in daily_train. Run daily maintainance operations.

        Args:
            void.

        Returns:
            void.
    """
    # Run only on Sunday - Thursday.
    if datetime.date.today().weekday() in [6, 0, 1, 2, 3]:

        # Log enter.
        logger.info("Daily train: Starting.")

        # Fetch all and save new rates.
        rates.main()

        # Run transformation and parameter selection for each strategy.
        for strategy_name in common.ALL_STRATEGIES:
            run(strategy_name)

        # Log exit.
        logger.info("Daily train: Done.")

    return

# Main.
if __name__ == "__main__":
    main()


