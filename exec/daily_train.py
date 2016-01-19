""" This module is responsible for updating data, retraining models as well as
    selecting the best strategy during the day. It should be scheduled to run
    at 18:00 on Sunday - Thursday.
"""

import common
import datetime
from data import rates

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
    transformer = __import__('strategies.' + module_name + '.transformer')
    transformer = getattr(getattr(transformer, module_name), 'transformer')

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
        # Fetch all and save new rates.
        rates.main()

        # Run transformation and parameter selection for each strategy.
        for strategy_name in common.ALL_STRATEGIES:
            run(strategy_name)


# Main.
if __name__ == "__main__":
    main()


