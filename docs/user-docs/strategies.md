# Strategy Guideline

### Basic idea
Foreign exchange (forex) is a market where price movements are usually
relatively small, comparing to, say, the stock market. Even with leverage,
because of the bid-ask spread, it is still very difficult to profit from
high frequency trading. Therefore the basic idea of MaLT is to restrict
its trading activities to a minimal granularity of daily, with the help of
Stop Loss (SL)/Take Profit (TP)/Trailing Stop (TS) orders.

More specifically, at each days end (right before 17:00 America/New York time),
MaLT will try to predict the __daily price change__ of the major currency
pairs for the next day. For example on 2016-03-03 at 16:59, MaLT may predict
that USD/CAD will increase by 55.5 pips between 2016-03-03 17:00 and
2016-03-04 17:00.

Then according to the prediction, MaLT decides whether to buy or sell the
currency pair, and if so, the number of units and the price of the orders.

The open trades will not be closed by MaLT during the trading day, though the
SL/TP/TS orders may be modified. The trades will either be closed by the
attached SL/TP/TS orders whenever they trigger, or by MaLT in exactly 24
hours, i.e. at 16:59 the next day regardless of its profit or loss.

Hence all MaLT's opening and closing activities happen around 17:00 every day.

### Strategy division and selection
All MaLT's strategies (named after accomplished mathematicians) work in the way
described above. However, different strategies predict the __daily price
change__ in different ways. Strategies are divided in such a way that each
strategy needs a distinct set and format of historical data, hence each has its
own data transformer.

During every trading day (by default at 17:10), MaLT's offline component will
update its historical data store, back-test all strategies on the updated
historical data, select the strategy that worked the best and serialize it
for next day's prediction.

### Individual strategies

#### Euler
Euler is the simplest strategy MaLT uses. It attempts to predict the next day's
price changes only using the previous day's daily candle, namely the open,
high, low and close of both bid and ask prices. That's 8 features in total.

#### Gauss
Gauss is slightly more advanced. It attempts to predict the next day's price
changes using five(5) previous days' daily candles. However, it will only use
the mid-point candles instead of both bid and ask, bringing it to `4 x 5 = 20`
features in total.

### Related information
- For more information about MaLT as a software application,
see documentation under `docs/dev-docs`.


