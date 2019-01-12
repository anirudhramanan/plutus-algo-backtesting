import abc

"""
Abstract class that needs to be implemented to define a strategy
"""


class SignalStrategy:
    __metaclass__ = abc.ABCMeta

    """
    Init method, this gets called when the network fetches the stock data.
    This is where you calculate all the required technical indicators which will be used in buy_signal or sell_signal
    
    You can store these results in the data_frame.
    """

    @abc.abstractmethod
    def init(self, stock_data):
        raise NotImplementedError("The method not implemented")

    """
    Define the buy strategy, eg buy on MA crossover
    Check out default implementation to learn more
    """

    @abc.abstractmethod
    def buy_signal(self, stock_data):
        raise NotImplementedError("The method not implemented")

    """
    Define the sell strategy, eg sell on MA crossover
    Check out default implementation to learn more
    """

    @abc.abstractmethod
    def sell_signal(self, stock_data):
        raise NotImplementedError("The method not implemented")

    """
    Define the profit target in percentage. 
    ie if profit target is 1, then the stock that has been bought will be sold as soon as it increases by 1%
    """

    def get_profit_target(self):
        raise NotImplementedError("The method not implemented")

    """
    Define the stop loss in percentage. 
    ie if stop loss is 1, then the stock that has been bought (instead of increasing, crashes) then it will be sold as soon
    as it decreases by 1%
    """

    def get_stop_loss_target(self):
        raise NotImplementedError("The method not implemented")
