def simple_moving_average(df, base, target, period):
    """
    Function to compute Simple Moving Average (SMA)
    This is a lagging indicator

    df - the data frame
    base - on which the indicator has to be calculated eg Close
    target - column name to store output
    period - period of the sma
    """
    df[target] = df[base].rolling(window=period).mean().round(2)
    return df


def exponential_moving_average(df, base, target, period):
    """
    Function to compute Exponential Moving Average (EMA)
    This is a lagging indicator

    df - the data frame
    base - on which the indicator has to be calculated eg Close
    target - column name to store output
    period - period of the ema
    """
    df[target] = df[base].ewm(ignore_na=False, min_periods=period, com=period, adjust=True).mean()
    return df


def moving_average_convergence_divergence(df, base, macd_target, macd_line_target, period_long=26, period_short=12,
                                          period_signal=9):
    """
    Function to compute MACD (Moving Average Convergence/Divergence)
    This is a lagging indicator

    df - the data frame
    base - on which the indicator has to be calculated eg Close
    macd_target - column name to store macd value
    macd_line_target - column name to store macd line
    period_long - period of the longer time frame
    period_short - period of the shorter time frame
    period_signal - period of the signal
    """
    short_ema_target = 'ema_{}'.format(period_short)
    long_ema_target = 'ema_{}'.format(period_long)

    df = exponential_moving_average(df, base, long_ema_target, period_long)
    df = exponential_moving_average(df, base, short_ema_target, period_short)

    df[macd_target] = df[short_ema_target] - df[long_ema_target]
    df[macd_line_target] = df[macd_target].ewm(ignore_na=False, min_periods=0, com=period_signal, adjust=True).mean()
    df = df.drop([short_ema_target, long_ema_target], axis=1)
    return df
