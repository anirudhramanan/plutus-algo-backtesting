class TaxCalculator:
    def __init__(self, data_frame):
        self.data_frame = data_frame

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

    @staticmethod
    def percentage(percent, whole):
        return (percent * whole) / 100.0
