import bitfinex
import pandas as pd
import numpy as np
import datetime
import logging
import time
import os
import asyncio
import aiohttp
from os.path import dirname, join


logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s','%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# function to read csv files
def _read_file(filename):
    return pd.read_csv(join(dirname(__file__), filename), index_col=0, parse_dates=True, infer_datetime_format=True)


# function call api
async def candles(symbol='btcusd', interval='1m', limit=1000, start=None, end=None, sort=-1):
    async with aiohttp.ClientSession() as session:
        resp = await session.get('https://api.bitfinex.com/v2/candles/trade:{}:t{}/hist?limit={}&start={}&end={}&sort=-1'.format(interval, symbol.upper(), limit, start, end, sort))
        results = await resp.json()
        return results

# Create a function to fetch the data
async def fetch_data(start=1364767200000, stop=1545346740000, symbol='btcusd', interval='1m', tick_limit=1000, step=60000000):
    # Create api instance
    api_v2 = bitfinex.bitfinex_v2.api_v2()

    data = []
    tasks = []
    
    for x in np.arange(start, stop, step):
        tasks.append(x)
    print(len(tasks))
    """
    start - step
    while start < stop:

        start = start + step
        end = start + step
        res = await candles(symbol=symbol, interval=interval, limit=tick_limit, start=start, end=end)
        data.extend(res)
        logger.info('Retrieving data from {} to {} for {}'.format(pd.to_datetime(start, unit='ms'),
                                                            pd.to_datetime(end, unit='ms'), symbol))
        time.sleep(1.5)
    return data
    """

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

SAVE_DIR = './data'

if os.path.exists(SAVE_DIR) is False:
    os.mkdir(SAVE_DIR)



async def main():
    for pair in pairs:
        csv_path = '{}/{}.csv'.format(SAVE_DIR, pair)
    
        df = pd.DataFrame()
        if os.path.exists(csv_path):
            logger.info("data file exists: {}".format(csv_path))
            df = _read_file(csv_path)
        else:
            logger.info("data file does not exists, creating a new csv: {}".format(csv_path))
    
        if not df.empty:
            logger.info(df.tail())
    
        pair_data = await fetch_data(start=t_start, stop=t_stop, symbol=pair, interval=bin_size, tick_limit=limit, step=time_step)
        continue 
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
        df.to_csv(csv_path)
        logger.info('Done saving data. Moving to next pair.')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    
    logger.info('Done retrieving data')
    loop.run_until_complete(main())
