def relative_strength_index(df, base, target, period=8):
    """
    Function to compute Relative Strength Index (RSI)

    df - the data frame
    base - on which the indicator has to be calculated eg Close
    target - column name to store output
    period - period of the rsi
    """
    delta = df[base].diff()
    up, down = delta.copy(), delta.copy()

    up[up < 0] = 0
    down[down > 0] = 0

    r_up = up.ewm(com=period - 1, adjust=False).mean()
    r_down = down.ewm(com=period - 1, adjust=False).mean().abs()

    df[target] = 100 - 100 / (1 + r_up / r_down)
    df[target].fillna(0, inplace=True)

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
