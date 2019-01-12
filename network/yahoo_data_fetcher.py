from network.stock_data_fetcher import StockDataFetcher
from helper.yahoo_finance import fetch

"""
Default fetcher to fetch stocks from yahoo finance
"""


class YahooDataFetcher(StockDataFetcher):
    def fetch_data(self, to_csv=False):
        stock_data = fetch(self.symbol, self.date_range, self.interval)
        stock_data = stock_data.round(2)

        if to_csv:
            stock_data.to_csv('data/{}.csv'.format(self.symbol), sep=',', encoding='utf-8')

        return stock_data
