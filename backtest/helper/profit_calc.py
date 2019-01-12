import pandas as pd


class ProfitTaxCalculator:
    def __init__(self, stock_data, number_of_stocks):
        self.data_frame = pd.DataFrame()
        self.stock_data = stock_data
        self.number_of_stocks = number_of_stocks

    def calculate_net_profit(self):
        self.calculate_rolling_profit(self.stock_data, self.number_of_stocks)
        self.calculate_turnover(self.number_of_stocks)
        self.calculate_total_tax(self.number_of_stocks, self.stock_data['Close'])
        self.data_frame['NET_PROFIT'] = self.data_frame['PL'] - self.data_frame['TAX']
        self.data_frame.round(2)
        return self.data_frame

    # ---- PRIVATE METHODS ----

    def calculate_brokerage_charges(self):
        self.data_frame['BRO_CHARGES'] = self.percentage(0.01, self.data_frame['TURNOVER'])

    def calculate_transaction_charges(self):
        self.data_frame['TRAN_CHARGES'] = self.percentage(0.0035, self.data_frame['TURNOVER'])

    def calculate_sebi_charges(self):
        self.data_frame['SEBI_CHARGES'] = self.percentage(0.00015, self.data_frame['TURNOVER'])

    def calculate_gst_charges(self):
        self.data_frame['GST'] = self.percentage(18, self.data_frame['BRO_CHARGES'] + self.data_frame['TRAN_CHARGES'])

    def calculate_stamp_duty_charges(self):
        self.data_frame['STAMP_DUTY'] = self.percentage(0.003, self.data_frame['TURNOVER'])

    def calculate_st_charges(self, number_of_stocks, close):
        self.data_frame['ST_CHARGES'] = \
            self.percentage(0.025, number_of_stocks * (close * self.data_frame['SIG_SHORT']))

    def calculate_total_tax(self, number_of_stocks, close):
        self.calculate_brokerage_charges()
        self.calculate_transaction_charges()
        self.calculate_sebi_charges()
        self.calculate_gst_charges()
        self.calculate_stamp_duty_charges()
        self.calculate_st_charges(number_of_stocks=number_of_stocks, close=close)
        self.data_frame['TAX'] = self.data_frame['ST_CHARGES'] + self.data_frame['STAMP_DUTY'] + \
                                 self.data_frame['GST'] + self.data_frame['SEBI_CHARGES'] + \
                                 self.data_frame['TRAN_CHARGES'] + self.data_frame['BRO_CHARGES']
        self.data_frame = self.data_frame.drop(columns=['ST_CHARGES', 'STAMP_DUTY', 'GST',
                                                        'SEBI_CHARGES', 'TRAN_CHARGES', 'BRO_CHARGES'])

    def calculate_turnover(self, number_of_stocks):
        self.data_frame['TURNOVER'] = number_of_stocks * abs(self.data_frame['POS']) + \
                                      number_of_stocks * abs(self.data_frame['POS_SHIFT'])
        self.clean_pl_turnover()

    def calculate_rolling_profit(self, stock_data, number_of_stocks):
        self.data_frame = stock_data[(stock_data['SIG_LONG'] + stock_data['SIG_SHORT']) != 0]
        self.data_frame['POS'] = ((stock_data['SIG_LONG'] + stock_data['SIG_SHORT'])
                                  * stock_data['Close'])
        self.data_frame['POS_SHIFT'] = self.data_frame['POS'].shift(1)
        self.data_frame['PL'] = (self.data_frame['POS'] + self.data_frame['POS_SHIFT']) * number_of_stocks

    def clean_pl_turnover(self):
        for i in range(len(self.data_frame)):
            if i % 2 == 0:
                self.data_frame['PL'].iloc[i] = 0
        for i in range(len(self.data_frame)):
            if i % 2 == 0:
                self.data_frame['TURNOVER'].iloc[i] = 0

    @staticmethod
    def percentage(percent, whole):
        return (percent * whole) / 100.0
