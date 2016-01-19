""" This module defines the Executor class for actually executing trades."""

import common
import http.client
import json

#===============================================================================
#   Classes:
#===============================================================================

class Executor():
    """ Class responsible for executing trades and orders."""

    def __init__(self, account_id):
        """ Initialize the Executor class.

            Args:
                account_id: int. Account number of the account.

            Returns:
                void.
        """
        self.account_id = account_id

        return


    def make_trade(self, instrument, units, **controls):
        """ Executes a market order.

            Args:
                instrument: string. The currency pair. e.g. 'EUR_USD'.
                units: signed int. Number of units for trade.
                    Positive for buy. Negative for sell.
                controls: named arguments, including:
                    stop_loss: float. Price for stop loss order.
                    take_profit: float. Price for take profit order.
                    trailing_stop: float. Pips for trailing stop order.

            Returns:
                trade_id: int or None. Return trade_id if opened a trade.
        """
        # Get the buy/sell side first.
        if units > 0:
            side = common.BUY
        elif units < 0:
            side = common.SELL
            units = -units
        else:
            return

        # Construct request strings.
        url = "/v1/accounts/{0}/orders".format(self.account_id)
        body = "instrument={0}&units={1}&side={2}&type=market". \
            format(instrument, units, side)

        # Add stop loss.
        if 'stop_loss' in controls and controls['stop_loss'] > 0:
            body += '&stopLoss={0}'.format(controls['stop_loss'])

        # Add take profit.
        if 'take_profit' in controls and controls['take_profit'] > 0:
            body += '&takeProfit={0}'.format(controls['take_profit'])

        # Add trailing stop.
        if 'trailing_stop' in controls and controls['trailing_stop'] > 0:
            body += '&trailingStop={0}'.format(controls['trailing_stop'])

        # Open connection. Send request. Get response.
        # TODO: Distinguish between game and trade.
        conn = http.client.HTTPSConnection(common.GAME_URL)
        conn.request("POST", url, body, common.GAME_HEADER)
        response = conn.getresponse()
        response_content = response.read().decode()
        conn.close()

        # Parse the JSON from the response and return the newly created trade id.
        trade_id = json.loads(response_content)['tradeOpened']['id']

        return trade_id


    def close_trade(self, trade_id):
        """ Close a given trade.

            Args:
                trade_id: int. id of the open trade to be closed.

            Returns:
                profit_loss: float. Profit or loss from closing the trade.
        """
        # Construct request strings.
        url = "/v1/accounts/{0}/trades/{1}".format(self.account_id, trade_id)

        # Open connection. Send request. Get response.
        conn = http.client.HTTPSConnection(common.GAME_URL)
        conn.request("DELETE", url, "", common.GAME_HEADER)
        response = conn.getresponse()
        response_content = response.read().decode()
        conn.close()

        # Parse the JSON from the response and return the profit_loss.
        try:
            profit_loss = json.loads(response_content)['profit']
        except KeyError:
            #TODO: What do we want to do when trying to close a non-existing trade?
            profit_loss = 0

        return profit_loss


    def get_all_trades(self):
        """ Get a list of all open trades.

            Args:
                void.

            Returns:
                trades. list of dicts. Each entry includes the details of a trade.
        """
        # Construct request url.
        url = ("/v1/accounts/{0}/trades".format(self.account_id))

        # Open connection. Send request. Get response.
        conn = http.client.HTTPSConnection(common.GAME_URL)
        conn.request("GET", url, "", common.GAME_HEADER)
        response = conn.getresponse()
        response_content = response.read().decode()
        conn.close()

        trades = json.loads(response_content)['trades']

        return trades


    def close_all_trades(self):
        """ Close all open trades.

            Args:
                void.

            Returns:
                void.
        """
        # TODO: Need a way to report success.
        trades = self.get_all_trades()

        for trade in trades:
            self.close_trade(trade['id'])

        return


