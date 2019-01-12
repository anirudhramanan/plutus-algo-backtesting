from backtest.stratergy.signal_strategy import SignalStrategy
from indicators.trend_indicators import simple_moving_average

"""
Strategy where the stock is bought / sold whenever the close price crosses the moving average
"""


class MACrossoverStrategy(SignalStrategy):

    def __init__(self):
        self.moving_average = 10

    def init(self, stock_data):
        stock_data = simple_moving_average(stock_data, 'Close', '{}MA'.format(self.moving_average), self.moving_average)
        stock_data['Prev_Close'] = stock_data['Close'].shift(1)
        stock_data['Prev_Open'] = stock_data['Open'].shift(1)
        stock_data['Candle'] = abs(stock_data['Open'] - stock_data['Close'])
        stock_data['Prev_Candle'] = abs(stock_data['Prev_Open'] - stock_data['Prev_Close'])

    def buy_signal(self, stock_data_row):
        if ((stock_data_row['Close'] > stock_data_row['{}MA'.format(self.moving_average)]) &
                (stock_data_row['Prev_Close'] < stock_data_row['{}MA'.format(self.moving_average)])):
            return True
        return False

    def sell_signal(self, stock_data_row):
        if ((stock_data_row['Close'] < stock_data_row['{}MA'.format(self.moving_average)]) &
                (stock_data_row['Prev_Close'] > stock_data_row['{}MA'.format(self.moving_average)])):
            return True
        return False

    def get_profit_target(self):
        return 1

    def get_stop_loss_target(self):
        return 1
