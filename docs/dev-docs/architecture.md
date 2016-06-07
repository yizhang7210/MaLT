# MaLT Architecture

### Components
MaLT consists of three(3) components: `data`, `exec` and `strategies`.

The `data` component is primarily responsible for retrieving and storing raw
historical forex exchange rates from OANDA, in the form of candles of various
granularities. The raw datasets are to be transformed and used differently
by different strategies.

The `exec` component is responsible for the online execution of MaLT. This is
the component that is connectd to OANDA's trading API to actually open, modify
and close trades.

The `strategies` component consists of a number of trading strategies. The end
goal of a strategy is to effectively and accurately predict the __profitable
price change__ of specific currency pairs for a trading day (i.e. from 17:00
of one day to 17:00 of the next), using some form of historical data. Each
strategy is also responsible for back-testing its parameters, selecting the
most profitable one, and serializing it for later use.

### Design convention and interfaces
There are a number of architectural design conventions that MaLT assumes for
it to be able to run properly.

1. Each strategy is named after a mathematician, e.g. Euler.
2. Under the directory of each strategy, there must be a module with the same
name as the strategy itself, but lower case, as well as a transformer module,
e.g. `strategies/euler/euler.py` and `strategies/euler/transformer.py` both
must exist.
3. The named modules above both must have a `main()` that will be run as part
of the `daily_train` routine.
4. The module same as the strategy name must contain a class of the same name.
The class must inherit from `strategies.base.BaseStrategy` and override the
empty methods., e.g. there must be a class `Euler(BaseStrategy)` defined in
`strategies/euler/euler.py`.

### Related information
- For details about MaLT's development guidlines,
see [MaLT Development Guidelines](development.md).
- For details about MaLT's individual packages,
see their corresponding `__init__.py` files.


