""" This is the malt.strategies.gauss package.

    Gauss is a (broad) strategy that attempts to make predictions based on
    daily candles. It uses the midpoint candles of the previous five (5) days
    as features and use machine learning to predict the profitable price
    change of the next day.
"""
