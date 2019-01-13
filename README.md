<img src="https://github.com/anirudhramanan/plutus-backtest/blob/master/icon.png" width="250" height="80" />

A python framework to run backtest on stocks using your own combination of algorithmic strategies and technical indicators.

## Sample Output Screenshot

![Sample](https://github.com/anirudhramanan/plutus-backtest/blob/master/sample_stock.png)

## Usage

<b>Checkout `plutus-demo.py` file for demo</b>

````
data_fetcher = YahooDataFetcher(symbol=config['symbol'], date_range=config['range'], interval=config['interval'])
strategy = MACrossoverStrategy()
plutus = Plutus(stock_fetcher=data_fetcher, signal_strategy=strategy)
plutus.backtest(BackTestType.SIGNAL_LONG)
````

Plutus takes in two arguments:

<b>StockDataFetcher</b> : a class used to fetch stock data. By default, use YahooDataFetcher which uses yahoo finance to fetch stock data based on the configuration.

<b>SignalStrategy</b> : This is where you define your buy and sell strategy. Implement the class and define your own strategy to buy and sell stocks. You can also specify the profit target and stop loss target.

Let us understand this with an example : 

When you go long (ie where you buy the stock first and sell later) and your buy condition meets, the trader will place a buy order. The order bought will only be sold if it meets any of the three conditions : 

  * Either your sell condition meets
  * Either the price hits the target you have defined 
  * Else the price hits the stop loss defined.

## Features

* Backtesting with your own custom strategy
* Create wishlist stocks and run tests against them
* Outputs profit / loss for each stock
* Support for some technical indicators
* Python3 support

## Technical Indicators

* Relative Strength Index (RSI) - Momentum Indicator
* Simple Moving Average (SMA) - Trend Indicator
* Exponential Moving Average (EMA) - Trend Indicator
* Moving Average Convergence Divergence (MACD) - Trend Indicator
* Average True Range (ATR) - Volatility Indicator
* Bollinger Band (BB) - Volatility Indicator

## Upcoming Features

* Plotting stocks 
* Adding support for more technical indicators
* Enable unit testing

## Contributing

The easiest way to contribute is by [forking the repo](https://help.github.com/articles/fork-a-repo/), making your changes and [creating a pull request](https://help.github.com/articles/creating-a-pull-request/).
