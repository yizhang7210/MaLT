""" This module is primarily responsible for retriving historical rates from
    a data source, parse them and save them to file.
"""

import csv
import http.client
import json
import common
import datetime

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
    header_string = "Bearer {0}".format(common.GAME_TOKEN)

    # Open connection. Send request. Get response.
    # TODO: Distinguish between game and trade.
    # TODO: Deal with connection errors/non-ideal responses.
    conn = http.client.HTTPSConnection(common.GAME_URL)
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
    # Set up the field names.
    date_len = len("2000-01-01")
    field_names = ['time', 'openBid', 'highBid', 'lowBid', 'closeBid',
                   'openAsk', 'highAsk', 'lowAsk', 'closeAsk', 'volume']

    # Write each candle line by line.
    with open(out_file, 'w') as csv_handle:
        # Write the headers first.
        writer = csv.writer(csv_handle, delimiter=' ')
        writer.writerow(field_names)

        # Initialize candle.
        candle = None
        for candle in candles:
            # Need to eliminate weekend candles.
            date = candle.get('time')[:date_len]
            date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')

            # The date needs to be Sunday - Thursday.
            if date_obj.weekday() in [6, 0, 1, 2, 3]:
                row = [date] + [candle.get(field) for field in field_names[1:]]
                writer.writerow(row)

def import_daily_candles():
    """ Fetch daily candles from common.START_DATE to date
        for all currency pairs.

        Args:
            void.

        Returns:
            void.
    """
    for instrument in common.ALL_PAIRS:
        # Set up the output files.
        out_file_path = "{0}/data/store/candles/daily/{1}.csv". \
                         format(common.PROJECT_DIR, instrument)
        start_date = common.START_DATE
        end_date = str(datetime.date.today() - datetime.timedelta(1))

        # Get the candles and write to file.
        candles = get_daily_candles(instrument, start_date, end_date)
        write_candles_to_csv(candles, out_file_path)

def main():
    """ Main in Data component.
        1. Fetch daily candles from common.START_DATE to date
        for all currency pairs.
    """
    import_daily_candles()


# Main.
if __name__ == "__main__":
    main()








