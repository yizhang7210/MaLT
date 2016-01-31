""" This module is responsible for transforming raw data to the appropriate
    feature format for strategy Euler.
"""

import common
logger = common.get_logger(__name__)
import csv
from strategies.euler import util

#===============================================================================
#   Functions:
#===============================================================================

def list_to_features(row, pip_factor):
    """ Return the row without the date, openBid and volume.
        Then take away the openBid price.

        Args:
            row: list of Strings. A row from data file in ./store/
            pip_factor: int. The multiplier for calculating pip from price.

        Returns:
            features: list of floats. The quantities are: highBid, lowBid,
                closeBid, openAsk, highAsk, lowAsk and closeAsk.
                All relative to openBid, and in pips.
    """
    row = common.list_to_float(row[1:-1])
    row = [x - row[0] for x in row[1:]]
    features = [common.price_to_pip(x, pip_factor) for x in row]

    return features


def candle_to_features(candle, pip_factor):
    """ Return the features but directly from candle information.

        Args:
            candle: dict. A dictionary representing information in a candle.
            pip_factor: int. The multiplier for calculating pip from price.

        Returns:
            features: list of floats. The quantities are: highBid, lowBid,
                closeBid, openAsk, highAsk, lowAsk and closeAsk.
                All relative to openBid, and in pips.
    """
    # Transform the candle to a list first.
    date = candle.get('time')[:common.DATE_LENGTH]
    row = [date] + [candle.get(field) \
        for field in common.CANDLE_FEATURES[1:]]

    # Then to the features.
    features = list_to_features(row, pip_factor)

    return features


def read_raw_file(input_file):
    """ Read the raw input file to a list.

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

    # Check validity of data since reading from file.
    # Last entry should be volume and should be large. The 200 is arbitrary.
    assert len(data[0]) == 10 and int(data[-1][9]) > 200

    # Log.
    logger.info("Read raw data from %s.", input_file)

    return data


def transform_row(row, next_row, pip_factor):
    """ Return the transformed row with features and target variable.

        Args:
            row: list of Strings. A row from the raw data file representing
                today's candle.
            next_row: list of Strings. The row representing tomorrow's candle.
            pip_factor: int. The multiplier for calculating pip from price.

        Returns:
            data_point: list of floats. Combine the features and the target.
    """
    features = list_to_features(row, pip_factor)
    target = util.get_price_change(next_row, pip_factor)

    data_point = features + [target]

    return data_point


def transform(input_file, output_file, pip_factor):
    """ Normalize daily candles.
        Features are:
            highBid, lowBid, closeBid, openAsk, highAsk,lowAsk,
            and closeAsk (all relative to openBid) in pips.
        Target variable is:
            Potential daily profitable price change in pips.
            If prices rise enough, we have: closeBid - openAsk (> 0), buy.
            If prices fall enough, we have: closeAsk - openBid (< 0), sell.
            if prices stay relatively still, we don't buy or sell. It's 0.

        Args:
            input_file: string. Name of the raw daily candle file, should
                be under the directory common.DAILY_CANDLES.
            output_file: string. Name of the normalized file, should be under
                ./store.
            pip_factor: int. The multiplier for calculating pip from price.

        Returns:
            void.
    """
    # Read the raw data and format.
    raw_data = read_raw_file(input_file)

    # Go through each line, build the features and targe variable.
    with open(output_file, 'w') as output_handle:
        writer = csv.writer(output_handle, delimiter=' ')

        for i in range(len(raw_data) - 1):
            row = transform_row(raw_data[i], raw_data[i + 1], pip_factor)
            writer.writerow(row)

    # Log.
    logger.info("Tranformed data to %s.", output_file)

    return


def main():
    """ Main in transforming data for strategy Euler."""
    for instrument in common.ALL_PAIRS:
        # Log enter.
        logger.info("Euler: transformer.main() Starting.")

        # Gather necessary data.
        in_file = common.get_raw_data(instrument)
        out_file = util.get_clean_data(instrument)
        pip_factor = common.get_pip_factor(instrument)

        # Transform.
        transform(in_file, out_file, pip_factor)

        # Log exit.
        logger.info("Euler: transformation done.")

    return


# Main.
if __name__ == "__main__":
    main()


