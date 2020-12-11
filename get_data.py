import bitfinex
import pandas as pd
import numpy as np
import datetime
import logging
import time
import os


logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s','%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Create a function to fetch the data
def fetch_data(start=1364767200000, stop=1545346740000, symbol='btcusd', interval='1m', tick_limit=1000, step=60000000):
    # Create api instance
    api_v2 = bitfinex.bitfinex_v2.api_v2()

    data = []
    start = start - step
    while start < stop:

        start = start + step
        end = start + step
        res = api_v2.candles(symbol=symbol, interval=interval, limit=tick_limit, start=start, end=end)
        data.extend(res)
        logger.info('Retrieving data from {} to {} for {}'.format(pd.to_datetime(start, unit='ms'),
                                                            pd.to_datetime(end, unit='ms'), symbol))
        time.sleep(1.5)
    return data


# Define query parameters
bin_size = '1m'
limit = 1000
time_step = 1000 * 60 * limit

t_start = datetime.datetime(2010, 1, 1, 0, 0)
t_start = time.mktime(t_start.timetuple()) * 1000

t_stop = datetime.datetime.now()
t_stop = time.mktime(t_stop.timetuple()) * 1000

api_v1 = bitfinex.bitfinex_v1.api_v1()
pairs = api_v1.symbols()

save_path = './data'

if os.path.exists(save_path) is False:
    os.mkdir(save_path)

for pair in pairs:
    pair_data = fetch_data(start=t_start, stop=t_stop, symbol=pair, interval=bin_size, tick_limit=limit, step=time_step)

    # Remove error messages
    ind = [np.ndim(x) != 0 for x in pair_data]
    pair_data = [i for (i, v) in zip(pair_data, ind) if v]

    # Create pandas data frame and clean data
    names = ['time', 'open', 'close', 'high', 'low', 'volume']
    df = pd.DataFrame(pair_data, columns=names)
    df.drop_duplicates(inplace=True)
    # df['time'] = pd.to_datetime(df['time'], unit='ms')
    df.set_index('time', inplace=True)
    df.sort_index(inplace=True)

    logger.info('Done downloading data. Saving to .csv.')
    save_path = '{}/bitfinex_{}.csv'.format(save_path, pair)
    df.to_csv(save_path)
    logger.info('Done saving data. Moving to next pair.')

logger.info('Done retrieving data')
