import datetime

import arrow
import pandas as pd
import requests


def fetch(symbol, data_range, data_interval):
    res = requests.get(
        'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}.NS?range={data_range}d&interval={data_interval}'.format(
            **locals()))
    data = res.json()
    body = data['chart']['result'][0]
    dt = datetime.datetime
    dt = pd.Series(map(lambda x: arrow.get(x).to('Asia/Calcutta').datetime.replace(tzinfo=None), body['timestamp']),
                   name='Date')
    df = pd.DataFrame(body['indicators']['quote'][0], index=dt)
    df = df.loc[:, ('open', 'high', 'low', 'close', 'volume')]
    df.fillna(method='ffill', inplace=True)  # removing NaN rows
    df.fillna(method='bfill', inplace=True)  # removing NaN rows
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']  # Renaming columns in pandas

    # done to square off values to 2 decimal places
    df = df.round(2)
    return df
