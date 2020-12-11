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
logger.setLevel(logging.DEBUG)

# function to read csv files
def _read_file(filename):
    return pd.read_csv(join(dirname(__file__), filename), index_col=0, parse_dates=True, infer_datetime_format=True)

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# function call api
async def candles(symbol='btcusd', interval='1m', limit=1000, start=None, end=None, sort=-1):
    async with aiohttp.ClientSession() as session:
        url = 'https://api.bitfinex.com/v2/candles/trade:{}:t{}/hist?limit={}&start={:.0f}&end={:.0f}&sort=-1'.format(interval, symbol.upper(), limit, start, end, sort)
        logger.debug("getting url: {}".format(url))
        resp = await session.get(url)
        results = await resp.json()
        if "error" in results:
            # recursive retry
            logger.error("Got rate limited. Trying symbol: {} start: {} end: {} again".format(symbol, start, end))
            return await candles(symbol=symbol, interval=interval, limit=limit, start=start, end=end)
        else:
            return results

# Create a function to fetch the data
async def fetch_data(start=1364767200000, stop=1545346740000, symbol='btcusd', interval='1m', tick_limit=1000, step=60000000):
    # Create api instance

    datas = []
    tasks = []

    # build a tasks list
    for current in np.arange(start, stop, step):
        logger.debug(current)
        tasks.append(candles(symbol=symbol, interval=interval, limit=tick_limit, start=current, end=current+step))

    # break up the task list into chunks
    for task_chunks in chunks(tasks, 90):
        resps = await asyncio.gather(*task_chunks)
        for resp in resps:
            datas.extend(resp)

    return datas

async def main():
    # Define query parameters
    bin_size = '1m'
    limit = 1000
    time_step = 1000 * 60 * limit
    
    t_start = datetime.datetime(2010, 1, 1, 0, 0)
    t_start = time.mktime(t_start.timetuple()) * 1000
    
    t_stop = datetime.datetime.now()
    t_stop = time.mktime(t_stop.timetuple()) * 1000
   
    async with aiohttp.ClientSession() as session:
        resp = await session.get('https://api.bitfinex.com/v1/symbols')
        pairs = await resp.json()
    
    SAVE_DIR = './data'
    
    if os.path.exists(SAVE_DIR) is False:
        os.mkdir(SAVE_DIR)

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
