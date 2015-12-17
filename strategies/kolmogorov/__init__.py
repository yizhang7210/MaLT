""" This strategy uses the open, close, high and low (both bid and ask)
    prices of the previous day as features and the profitable price change
    of the next day as target for learning.

    This strategy formulate the problem as a classification problem where
    the learner tries to classify the next day's price change into 3 different
    classes: large rise, large drop and not much change (regarding a threshold)
    so that it can decide to buy, sell or do nothing respectively.
"""
