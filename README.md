# plutus-backtest

A python platform to backtest stocks using your own combination of strategies and technical indicators. 

## Usage ?

````
data_fetcher = YahooDataFetcher(symbol=config['symbol'], date_range=config['range'], interval=config['interval'])
strategy = MACrossoverStrategy()
plutus = Plutus(stock_fetcher=data_fetcher, signal_strategy=strategy)
plutus.backtest(BackTestType.SIGNAL_LONG)
````

Plutus takes in two arguments:

<b>StockDataFetcher</b> : a class used to fetch stock data. By default, use YahooDataFetcher which uses yahoo finance to fetch stock data based on the configuration.

<b>SignalStrategy</b> : This is where you define your buy and sell strategy. Implement the class and define your own strategy to buy and sell stocks. You can also specify the profit target and stop loss target

Let us understand this with an example : 

When you go long (ie where you buy the stock first and sell later) and your buy condition meets, the trader will place a buy order. The order bought will only be sold if it meets any of the three conditions : 

  * Either your sell condition meets
  * Either the price hits the target you have defined 
  * Else the price hits the stop loss defined.
  
<b>Checkout `plutus-demo.py` file for demo run</b>

## Features ?

* Backtesting with your own custom strategy

* Create wishlist stocks and run the test against them

* Support for some technical indiactors

* Python3 support

## Upcoming Features ?

* Plotting stocks 

* Adding more technical indicators
