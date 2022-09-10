from indicators.trend_indicators import exponential_moving_average, vwap
from strategy.signal_strategy import SignalStrategy

"""
Strategy where the stock is bought / sold whenever the close price crosses the moving average
"""


class VWAPStrategy(SignalStrategy):

    def init(self, stock_data):
        stock_data = exponential_moving_average(stock_data, "Close", "7ema", 7)
        stock_data = exponential_moving_average(stock_data, "Close", "25ema", 25)
        stock_data = vwap(stock_data)
        stock_data = exponential_moving_average(stock_data, "Vwap", "mvwap", 7)

        stock_data['prev_7ema'] = stock_data['7ema'].shift(1)
        stock_data['prev_25ema'] = stock_data['25ema'].shift(1)

    def buy_signal(self, stock_data_row):
        if stock_data_row["prev_7ema"] < stock_data_row["25ema"] < stock_data_row["7ema"] \
                and stock_data_row["Close"] * 1.02 > stock_data_row["Vwap"] >= stock_data_row["mvwap"]:
            return True
        return False

    def sell_signal(self, stock_data_row):
        return False

    def get_profit_target(self):
        return 2

    def get_stop_loss_target(self):
        return 1
