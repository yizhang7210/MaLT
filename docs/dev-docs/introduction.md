# Developer Introduction
Welcome to MaLT.

MaLT as an application effectively consists of two(2) cron jobs that get run
every day.

`malt/exec/daily_run.py` should be run every day at 16:59 America/New York
time. At day's close, i.e. 16:59, this job will close all trades that were
opened in the previous day. At day's open, i.e. right after 17:00, it will
read a serialized strategy and its parameters that deemed most profitable from
historical testing, and call `execute` on the strategy object. Typically the
`execute` method will make prediction about the price changes of various
currencies for the next day, and open trades/orders accordingly.

`malt/exec/daily_train.py` can be run every day at any time between 17:00 and
23:59. By default it runs at 17:10. It starts by fetching the new data from the
previous trading day. Then it goes through each strategy to update their data
stores, retrain their learning models, selecting the best parameters based on
some profitability metric and serialize it to the `malt/exec/daily_strategy`
directory.

### Related information
- For details about MaLT's software architecture,
see [MaLT Architecture](architecture.md).
- For details about MaLT's individual packages,
see their corresponding `__init__.py` files.
- For details about MaLT's development guidlines,
see [MaLT Development Guidelines](development.md).


