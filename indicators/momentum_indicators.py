from ta.momentum import rsi


def relative_strength_index(df, base, target, period=8):
    """
    Function to compute Relative Strength Index (RSI)

    df - the data frame
    base - on which the indicator has to be calculated eg Close
    target - column name to store output
    period - period of the rsi
    """
    df[target] = rsi(df[base], window=period)
    return df


def stochastic(df, target, period=8):
    """Stochastic Oscillator
    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    smin = df['Low'].rolling(period, min_periods=0).min()
    smax = df['High'].rolling(period, min_periods=0).max()

    df[target] = 100 * (df['Close'] - smin) / (smax - smin)
    df[target] = df[target].round(2)
    df[target].fillna(0, inplace=True)

    return df
