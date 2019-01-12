from backtest.plutus import Plutus
import json
import time
import warnings

import pandas as pd

from backtest.helper.backtest_type import BackTestType
from backtest.network.yahoo_data_fetcher import YahooDataFetcher
from backtest.plutus import Plutus
from backtest.stratergy.ma_crossover_strategy import MACrossoverStrategy

warnings.filterwarnings('ignore')


def call_strategy(config):
    data_fetcher = YahooDataFetcher(symbol=config['symbol'], date_range=config['range'], interval=config['interval'])
    strategy = MACrossoverStrategy()
    plutus = Plutus(stock_fetcher=data_fetcher, signal_strategy=strategy)
    plutus.backtest(BackTestType.SIGNAL_LONG)
    positions = plutus.calculate_profit(config['shares'])

    print('Number of buy orders   : {}'.format(plutus.number_of_buy_orders()))
    print('Number of sell orders  : {}'.format(plutus.number_of_sell_orders()))
    print('Total number of stocks : {}'.format(1))
    print('Turnover               : {}'.format(positions['TURNOVER'].sum()))
    print('Total TAX              : {:.2f}'.format(positions['TAX'].sum()))
    print('Total PL               : {:.2f}'.format(positions['PL'].sum()))
    print('Total PL after TAX     : {:.2f}'.format(positions['NET_PROFIT'].sum()))

    return config['symbol'], plutus.number_of_buy_orders(), plutus.number_of_sell_orders(), positions[
        'NET_PROFIT'].sum(), positions['TAX'].sum(), positions['PL'].sum(), positions['TURNOVER'].sum()


profit_data = []

with open('config/stocks.json') as f:
    stocks = json.load(f)

for stock_config in stocks:
    ticker_data = []
    ticker, buy_orders, sell_orders, n_profit, tax, profit, turnover = call_strategy(config=stock_config)
    ticker_data.append(ticker)
    ticker_data.append(buy_orders)
    ticker_data.append(sell_orders)
    ticker_data.append(profit)
    ticker_data.append(tax)
    ticker_data.append(n_profit)
    ticker_data.append(turnover)
    profit_data.append(ticker_data)
    time.sleep(2)

portfolio = pd.DataFrame(data=profit_data, columns=['Symbol', 'BO', 'SO', 'PL', 'TAX', 'NPL', 'T'])
print('\n')
print(portfolio.round(2).sort_values(by=['NPL'], ascending=False))
print('\nTotal Trading Orders : {}'.format(int((portfolio['BO'].sum() + portfolio['SO'].sum()) / 2)))
print('Turnover             : {}'.format(portfolio['T'].sum()))
print('Total PL             : {}'.format(int(portfolio['PL'].sum())))
print('Total TAX            : {}'.format(int(portfolio['TAX'].sum())))
print('Total NPL            : {}'.format(int(portfolio['NPL'].sum())))
