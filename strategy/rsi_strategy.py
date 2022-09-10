from indicators.momentum_indicators import relative_strength_index
from indicators.volatility_indicator import bollinger_band
from strategy.signal_strategy import SignalStrategy

"""
Strategy where the stock is bought / sold whenever the close price crosses the moving average
"""


class RSIStrategy(SignalStrategy):

    def init(self, stock_data):
        stock_data = relative_strength_index(stock_data, "Close", "RSI", 8)
        stock_data = bollinger_band(stock_data, "Close", "BB-T", "BB-B", 20)

    def buy_signal(self, stock_data_row):
        if stock_data_row["Close"] < stock_data_row["BB-B"] and stock_data_row["RSI"] <= 8:
            return True
        return False

    def sell_signal(self, stock_data_row):
        if stock_data_row["Close"] > stock_data_row["BB-T"] and stock_data_row["RSI"] >= 70:
            return True
        return False

    def get_profit_target(self):
        return 1

    def get_stop_loss_target(self):
        return 1
