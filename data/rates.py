""" This module is primarily responsible for retriving historical rates from
    a data source, parse them and save them to file.
"""

import csv
import http.client
import json
import data.common
import datetime
import os

def get_daily_candles(instrument, start_date, end_date):
    """ Obtain a list of daily bid-ask candles for the given instrument.
        Candles are from start_date to end_date, both inclusive.
        Days with no market activities do NOT have candles.
        Candles are aligned according to New York time. Exactly 5 per week.

        Args:
            instrument: String. The currency pair. e.g. "EUR_USD".
            start_date: String. Formatted start date. e.g. "2015-11-24".
            end_date: Sting. Formatted end date. e.g. "2015-11-28".

        Returns:
            candles: List of dictionaries, each representing a daily candle.
            Example:
                [{'volume': 28947, 'highAsk': 1.07594, 'openAsk': 1.0746,
                'lowAsk': 1.06757, 'lowBid': 1.06741, 'closeBid': 1.06853,
                'closeAsk': 1.06871, 'openBid': 1.07378,
                'time': '2015-11-15T22:00:00.000000Z',
                'complete': True, 'highBid': 1.07574}, {...}]
    """

    # Construct request string.
    request_string = ("/v1/candles?instrument={0}&start={1}&end={2}&"
                      "candleFormat=bidask&granularity=D&dailyAlignment=17&"
                      "alignmentTimezone=America%2FNew_York"). \
                     format(instrument, start_date, end_date)
    header_string = "Bearer {0}".format(data.common.GAME_TOKEN)

    # Open connection. Send request. Get response.
    # TODO: Distinguish between game and trade.
    # TODO: Deal with connection errors/non-ideal responses.
    conn = http.client.HTTPSConnection(data.common.GAME_URL)
    conn.request("GET", request_string, "", {"Authorization" : header_string})
    response = conn.getresponse()
    response_content = response.read().decode()
    conn.close()

    # Parse the JSON from the response and select 'candles'.
    candles = json.loads(response_content)['candles']
    return candles


def write_candles_to_csv(candles, out_file):
    """ Write the candles to the out_file file as a csv.

        Args:
            candles: List of dictinoaries. List of candles containing open,
                close, high and low, time and volume.
            out_file: String. Location of the output file.

        Returns:
            void.
    """
    # TODO: Check candles are valid, non-empty and have the right fields.

    # Set up the field names.
    date_len = len("2000-01-01")
    field_names = ['time', 'openBid', 'highBid', 'lowBid', 'closeBid',
                   'openAsk', 'highAsk', 'lowAsk', 'closeAsk', 'volume']

    def get_short_field(field):
        """ Have a local function fetching the fields and shorten it."""
        return str(candle.get(field))[:date_len]

    # Write each candle line by line.
    with open(out_file, 'w') as csv_handle:
        writer = csv.writer(csv_handle, delimiter=' ')
        writer.writerow(field_names)
        candle = None
        for candle in candles:
            writer.writerow([get_short_field(field) for field in field_names])


def import_daily_candles():
    """ Fetch daily candles from 2006-01-01 to date for all currency pairs.

        Args:
            void.

        Returns:
            void.
    """
    project_dir = os.environ['PYTHONPATH']
    for instrument in data.common.ALL_PAIRS:
        # Set up the output files.
        out_file_path = "{0}/data/store/candles/daily/{1}.csv". \
                         format(project_dir, instrument)
        start_date = "2006-01-01"
        end_date = str(datetime.date.today() - datetime.timedelta(1))

        # Get the candles and write to file.
        candles = get_daily_candles(instrument, start_date, end_date)
        write_candles_to_csv(candles, out_file_path)

def main():
    """ Main in Data component.
        1. Fetch daily candles from 2006-01-01 to date for all currency pairs.
    """
    import_daily_candles()


# Main.
if __name__ == "__main__":
    main()








