""" This module is responsible for transforming raw data to
    the appropriate format for strategy Euler.
"""

import csv
import common
from strategies import util
from strategies.euler import euler


#===============================================================================
#   Functions:
#===============================================================================

def build_features(row, pip_multiplier):
    """ Return the row without the date, openBid and volume.
        Then take away the openBid price.

        Args:
            row: list of Strings. A row from data file in ./store/
            pip_multiplier: int. The multiplier for calculating pip from price.

        Returns:
            features: list of floats. The quantities are: highBid, lowBid,
                closeBid, openAsk, highAsk, lowAsk and closeAsk.
                All relative to openBid, and in pips.
    """
    row = util.list_to_float(row[1:-1])
    row = [x - row[0] for x in row[1:]]
    features = [util.price_to_pip(x, pip_multiplier) for x in row]
    return features


def read_raw_file(input_file):
    """ Read the raw input file to a nice format.

        Args:
            input_file: string. Location of the input raw data file.

        Returns:
            data: list of list of Strings. Each entry is a daily candle.
                Within a daily candle, it's date, OHLC of bidAsk and volume.
    """
    with open(input_file, 'r') as input_handle:
        # First line is header and last line is empty.
        data = input_handle.read().split('\n')[1:-1]

    data = [x.split(' ') for x in data]

    return data


def transform_row(row, next_row, pip_multiplier):
    """ Return the transformed row with features and target variable.

        Args:
            row: list of Strings. A row from the raw data file representing
                today's candle.
            next_row: list of Strings. The row representing tomorrow's candle.
            pip_multiplier: int. The multiplier for calculating pip from price.

        Returns:
            row: list of floats. Combine the features and the target.
    """
    features = build_features(row, pip_multiplier)
    target = euler.get_price_change(next_row, pip_multiplier)

    return features + [target]


def transform(input_file, output_file, pip_multiplier):
    """ Normalize daily candles.
        Features are:
            highBid, lowBid, closeBid, openAsk, highAsk,lowAsk,
            and closeAsk (all relative to openBid) in pips.
        Target variable is:
            potential daily benefical price change in pips.
            If prices rise enough, we have: closeBid - openAsk (> 0), buy.
            If prices fall enough, we have: closeAsk - openBid (< 0), sell.
            if prices stay relatively still, we don't buy or sell. It's 0.

        Args:
            input_file: string. Name of the raw daily candle file, should
                be under common.DAILY_CANDLES.
            output_file: string. Name of the normalized file, should be under
                ./store.
            pip_multiplier: int. Factor for converting price to pips.

        Returns:
            void.
    """
    # Read the raw data and format.
    raw_data = read_raw_file(input_file)

    # Go through each line, build the features and targe variable.
    with open(output_file, 'w') as output_handle:
        writer = csv.writer(output_handle, delimiter=' ')

        for i in range(len(raw_data) - 1):
            row = transform_row(raw_data[i], raw_data[i + 1], pip_multiplier)
            writer.writerow(row)


def main():
    """ Main in transforming data for strategy Euler."""

    for instrument in common.ALL_PAIRS:
        in_file = euler.get_raw_data(instrument)
        out_file = euler.get_clean_data(instrument)
        pip_multiplier = util.get_pip_multiplier(instrument)
        transform(in_file, out_file, pip_multiplier)

# Main.
if __name__ == "__main__":
    main()


