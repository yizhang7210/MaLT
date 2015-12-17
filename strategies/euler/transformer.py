""" This package is responsible for transforming raw data to
    the appropriate format for this strategy: Euler.
"""

import csv
import common

def price_to_pip(price, pip_multiplier):
    """ Numbers are format to 1 decimal places in pips."""
    pip = price * pip_multiplier
    return "{0:.1f}".format(pip)


def list_to_float(lst):
    """ Change the entire list to float."""
    # TODO: how do we deal with exceptions?
    return [float(x) for x in lst]


def build_features(row, pip_multiplier):
    """ Return the row without the date, openBid and volume.
        Then take away the openBid price.
    """
    row = list_to_float(row[1:-1])
    features = [x - row[0] for x in row[1:]]
    features = [price_to_pip(x, pip_multiplier) for x in features]
    return features


def build_target(row, pip_multiplier):
    """ If closeBid - openAsk > 0. Can buy.
        If closeAsk - openBid < 0. Can sell.
        Otherwise do nothing.
    """
    # TODO: use dictionary instead of indices.
    row = list_to_float(row[1:-1])
    if row[3] - row[4] > 0:
        diff = row[3] - row[4]
    elif row[7] - row[0] < 0:
        diff = row[7] - row[0]
    else:
        diff = 0

    return [price_to_pip(diff, pip_multiplier)]


def transform(input_file, output_file, pip_multiplier):
    """ Normalize daily candles.
        Features are:
            highBid, lowBid, closeBid, openAsk, highAsk,lowAsk,
            and closeAsk (all relative to openBid) IN PIPS.
        Target variable is:
            potential daily benefical price change IN PIPS.
            If prices rise enough, we have: closeBid - openAsk (> 0), buy.
            If prices fall enough, we have: closeAsk - openBid (< 0), sell.
            if prices stay relatively still, we don't buy or sell. It's 0.

        Args:
            input_file: String. Name of the raw daily candle file.
                e.g. MaLT/data/store/candles/daily/EUR_USD.csv
            output_file: String. Name of the normalized file.
                e.g. MaLT/strategies/ar_daily/store/EUR_USD.csv
            pip_multiplier: Int. Factor for converting price to pips.
                e.g. 100 for USD_JPY and 10000 for all others.
        Returns:
            void.
    """

    with open(input_file, 'r') as input_handle:
        reader = csv.reader(input_handle, delimiter=' ')
        # Skip header line.
        next(reader)
        with open(output_file, 'w') as output_handle:
            writer = csv.writer(output_handle, delimiter=' ')

            # Initialize iterator.
            thisrow = next(reader)
            nextrow = next(reader)
            while True:
                try:
                    features = build_features(thisrow, pip_multiplier)
                    target = build_target(nextrow, pip_multiplier)
                    writer.writerow(features + target)
                    thisrow = nextrow
                    nextrow = next(reader)
                except StopIteration:
                    break

def main():
    """ Main in transforming data for ar_daily strategy."""

    for instrument in common.ALL_PAIRS:
        in_file = "{0}/data/store/candles/daily/{1}.csv". \
                   format(common.PROJECT_DIR, instrument)
        out_file = "store/{0}.csv".format(instrument)

        if 'JPY' in instrument:
            transform(in_file, out_file, 100)
        else:
            transform(in_file, out_file, 10000)

# Main.
if __name__ == "__main__":
    main()


