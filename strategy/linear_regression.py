from math import sqrt

from strategy.signal_strategy import SignalStrategy

"""
Strategy where the stock is bought / sold whenever the close price crosses the moving average
"""


class LinearRegression(SignalStrategy):

    def __init__(self):
        self.moving_average = 10
        self.linear_reg_line_start = 0
        self.linear_reg_line_end = 0
        self.sd1_low = 0
        self.sd2_low = 0
        self.sd3_low = 0

    def init(self, stock_data):
        close_prices = stock_data["Close"].tolist()

        sum_x = 0.0
        sum_y = 0.0
        sum_x_sqr = 0.0
        sum_xy = 0.0

        i = 0
        for s in close_prices:
            per = i + 1.0
            sum_x = sum_x + per
            sum_y = sum_y + s
            sum_x_sqr = sum_x_sqr + per * per
            sum_xy = sum_xy + s * per
            i = i + 1

        slope = (200 * sum_xy - sum_x * sum_y) / (200 * sum_x_sqr - sum_x * sum_x)
        intercept = sum_y / 200 - slope * sum_x / 200 + slope

        std_dev_acc = 0.0
        periods = 200 - 1
        val = intercept

        for s in close_prices:
            price = s - val
            std_dev_acc = std_dev_acc + price * price
            val = val + slope

        std_dev = sqrt(std_dev_acc / periods)
        self.linear_reg_line_end = intercept + slope * (200 - 1)
        self.linear_reg_line_start = intercept
        self.sd1_low = self.linear_reg_line_end - std_dev
        self.sd2_low = self.linear_reg_line_end - std_dev * 2
        self.sd3_low = self.linear_reg_line_end - std_dev * 3

    def buy_signal(self, stock_data_row):
        close_price = stock_data_row["Close"]
        if (((close_price[0] < self.sd2_low) or (
                close_price[0] < self.sd3_low)) and self.linear_reg_line_end > self.linear_reg_line_start):
            return True
        return False

    def sell_signal(self, stock_data_row):
        return False

    def get_profit_target(self):
        return 1

    def get_stop_loss_target(self):
        return 1
