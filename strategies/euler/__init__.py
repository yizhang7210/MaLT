""" This strategy uses the open, close, high and low (both bid and ask)
    prices of the previous day as features and the profitable price change
    of the next day as target for learning.

    This strategy formulate the problem as a regression problem where the
    learner tries to predict the next day's price change so that it can
    decide the action as well as the number of units for the next day.
"""
