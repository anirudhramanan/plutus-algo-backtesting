import pandas as pd

from backtest.helper.yahoo_finance import fetch_stock_data


class Portfolio:
    def __init__(self):
        self.nifty_50_stocks = [
            "VEDL", "MARUTI", "BPCL", "TATAMOTORS",
            "ADANIPORTS", "HINDALCO", "INDUSINDBK",
            "IOC", "HINDPETRO", "HEROMOTOCO",
            "M&M", "ULTRACEMCO", "BAJAJFINSV",
            "TATASTEEL", "HDFC", "BHARTIARTL",
            "EICHERMOT", "JSWSTEEL", "ASIANPAINT",
            "BAJAJ-AUTO", "AXISBANK", "YESBANK",
            "IBULHSGFIN", "ITC", "LT",
            "UPL", "KOTAKBANK", "HDFCBANK",
            "HINDUNILVR", "ONGC", "TITAN",
            "RELIANCE", "GAIL", "POWERGRID",
            "NTPC", "COALINDIA", "ICICIBANK",
            "SUNPHARMA", "INFRATEL", "GRASIM",
            "SBIN", "HCLTECH", "INFY", "TCS",
            "BAJFINANCE", "ZEEL", "CIPLA", "DRREDDY",
            "WIPRO", "TECHM"]

        self.all_stock_data = pd.DataFrame(columns=['Stock', 'Volume', 'High', 'Low'])

        i = 0
        for stock in self.nifty_50_stocks:
            stock_data = fetch_stock_data(stock, 1, '1d')
            self.all_stock_data.loc[i] = [stock, stock_data['Volume'].mean(), stock_data['High'].mean(),
                                          stock_data['Low'].mean()]
            i = i + 1

        print('Fetched data for all nifty 50 stocks')

    # Gives top n traded stocks by volume
    def based_on_volume(self, n):
        stocks = self.all_stock_data.sort_values(by=['Volume'], ascending=False)
        print('Highest traded stocks by volume')
        print(stocks.head(n))

    # Gives top n traded stocks by volume
    def based_on_price_volatility(self, n):
        self.all_stock_data['High-Low'] = self.all_stock_data['High'] - self.all_stock_data['Low']
        stocks = self.all_stock_data.sort_values(by=['High-Low'], ascending=False)
        print('Highest traded stocks by price volatility')
        print(stocks.head(n))
