from helper.backtest_type import BackTestType
from helper.profit_calc import ProfitTaxCalculator
from network.stock_data_fetcher import StockDataFetcher
from strategy.signal_strategy import SignalStrategy


class Plutus:
    def __init__(self, stock_fetcher, signal_strategy):
        if not issubclass(type(stock_fetcher), StockDataFetcher):
            raise TypeError('stock_fetcher should be of type StockDataFetcher')

        if not issubclass(type(signal_strategy), SignalStrategy):
            raise TypeError('signal_strategy should be of type SignalStrategy')

        self.stock_data = stock_fetcher.fetch_data()
        self.stock_data['SIG_LONG'] = 0
        self.stock_data['SIG_SHORT'] = 0
        self.signal_strategy = signal_strategy
        self.signal_strategy.init(self.stock_data)

    def backtest(self, type):
        if type != BackTestType.SIGNAL_SHORT and type != BackTestType.SIGNAL_LONG:
            raise TypeError("type should be SIGNAL_SHORT or SIGNAL_LONG")

        if type == BackTestType.SIGNAL_LONG:
            buy_position = False
            buy_price = 0
            for index, row in self.stock_data.iterrows():
                if self.signal_strategy.buy_signal(row):
                    # we have a buy call, check there is no previous buy which
                    # has not been sold yet
                    if not buy_position:
                        self.stock_data.at[index, 'SIG_LONG'] = -1
                        buy_price = row['Close']
                        buy_position = True
                        continue

                target = buy_price + buy_price * self.signal_strategy.get_profit_target() / 100
                stop_loss = buy_price - buy_price * self.signal_strategy.get_stop_loss_target() / 100
                if row['Close'] > target or row['Close'] < stop_loss or self.signal_strategy.sell_signal(row):
                    # we have a sell call, check there is a buy position
                    # which needs to be sold
                    if buy_position:
                        self.stock_data.at[index, 'SIG_SHORT'] = 1
                        buy_position = False

        if type == BackTestType.SIGNAL_SHORT:
            sell_position = False
            sell_price = 0
            for index, row in self.stock_data.iterrows():
                if self.signal_strategy.sell_signal(row):
                    # we have a buy call, check there is no previous buy which
                    # has not been sold yet
                    if not sell_position:
                        self.stock_data.at[index, 'SIG_SHORT'] = 1
                        sell_price = row['Close']
                        sell_position = True
                        continue

                target = sell_price - sell_price * self.signal_strategy.get_profit_target() / 100
                stop_loss = sell_price + sell_price * self.signal_strategy.get_stop_loss_target() / 100
                if row['Close'] > target or row['Close'] < stop_loss or self.signal_strategy.buy_signal(row):
                    # we have a sell call, check there is a buy position
                    # which needs to be sold
                    if sell_position:
                        self.stock_data.at[index, 'SIG_LONG'] = -1
                        sell_position = False

        self.mark_exit_position_if_any()

    def number_of_buy_orders(self):
        if 'SIG_LONG' not in self.stock_data.columns:
            raise Exception("Use one of the indicators in your strategy")
        return -1 * self.stock_data['SIG_LONG'].sum()

    def number_of_sell_orders(self):
        if 'SIG_SHORT' not in self.stock_data.columns:
            raise Exception("Use one of the indicators in your strategy")
        return self.stock_data['SIG_SHORT'].sum()

    def calculate_profit(self, number_of_stocks):
        profit_calc = ProfitTaxCalculator(self.stock_data, number_of_stocks)
        return profit_calc.calculate_net_profit()

    # ---- PRIVATE METHODS ---- #

    def mark_exit_position_if_any(self):
        for date, row in self.stock_data.iterrows():
            if date.time().hour == 15 and date.time().minute == 25:
                # if it's 3.25 check for any open position for that day and close if necessary
                day_stock_data = self.stock_data.loc[self.stock_data.index.to_series().dt.date == date.date()]
                position_sum = (day_stock_data['SIG_LONG'] + day_stock_data['SIG_SHORT']).sum()
                if position_sum < 0:
                    self.stock_data.at[date, 'SIG_SHORT'] = 1
                elif position_sum > 0:
                    self.stock_data.at[date, 'SIG_LONG'] = -1
