import abc

"""
Abstract class that needs to be implemented to fetch the stocks
"""


class StockDataFetcher:
    __metaclass__ = abc.ABCMeta

    """
    symbol : stock symbol
    date_range : in numbers ie if date_range is 2, data is fetched for last 2 days
    interval (2m, 5m etc) 
    """

    def __init__(self, symbol, date_range, interval):
        self.symbol = symbol
        self.date_range = date_range
        self.interval = interval

    """
    implement your fetch method, enable to_csv to store the result in csv file
    """

    @abc.abstractmethod
    def fetch_data(self, to_csv=False):
        raise NotImplementedError("The method not implemented")
