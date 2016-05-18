""" This is the test module for executor.py."""

# External imports
import time
import unittest

# Internal imports
from malt import common
from malt.exec.executor import Executor

#===============================================================================
#   Classes:
#===============================================================================

class TestExecutor(unittest.TestCase):
    """ Class for testing executor."""

    def setUp(self):
        """ Set up temporary files."""
        pass


    def tearDown(self):
        """ Delete temporary files."""
        pass


    def test_open_close_trades(self):
        """ Test open and close of trades."""
        # Get an executor object.
        executor = Executor(common.GAME_DEV_ACCOUNT)

        # Close all open trades first.
        executor.close_all_trades()

        # Now make a new trade.
        sltpts = {'stop_loss': 8.0, 'take_profit': 216.8, 'trailing_stop': 8.3}
        buy_trade = executor.make_trade('USD_JPY', 213, **sltpts)

        # Close it.
        profit_loss = executor.close_trade(buy_trade)
        self.assertTrue(profit_loss != 0)

        # Pause for rate limiting reasons.
        time.sleep(1)

        # Open a sell trade.
        sltpts = {'stop_loss': 3.0, 'take_profit': 0.2, 'trailing_stop': 40}
        sell_trade = executor.make_trade('USD_CAD', -55, **sltpts)

        # Make sure it's there.
        trades = executor.get_all_trades()
        self.assertTrue(len(trades) == 1)
        self.assertTrue(trades[0]['id'] == sell_trade)

        # Now close all of them.
        executor.close_all_trades()

        # Make sure there's nothing left.
        trades = executor.get_all_trades()
        self.assertTrue(len(trades) == 0)

        return


#===============================================================================
#   Functions:
#===============================================================================

# Main.
if __name__ == "__main__":
    unittest.main()


