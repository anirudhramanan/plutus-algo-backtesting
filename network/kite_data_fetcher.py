import pandas as pd

from helper.kite_login import get_historical_data
from network.stock_data_fetcher import StockDataFetcher

"""
Default fetcher to fetch stocks from yahoo finance
"""


class KiteDataFetcher(StockDataFetcher):
    def fetch_data(self, to_csv=False):
        stock_data = get_historical_data("260105", "2022-05-10", "2022-06-10", "minute")
        result = pd.DataFrame(stock_data)
        result = result.rename(
            columns={'close': 'Close', 'high': 'High', 'low': 'Low', 'volume': 'Volume', 'open': 'Open'})
        return result
