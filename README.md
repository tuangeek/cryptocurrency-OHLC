# cryptocurrency OHLC

---

This dataset contains the historical trading data (OHLC) of more than 400 trading pairs at 1 minute resolution reaching back until the year 2013.

# Features
- historical trading data (OHLC)
- 400+ trading pairs (btcusd , ethusd, btceth, ...)
- 1 minute resolution
- Data 2013 - Present
- CSV files

## Installation

### Requirements

python3+

### Install Dependencies

```sh
pip install requests pip install requests bitfinex-tencars pandas
```

Or via requirements.txt:
```sh
pip install -r requirements.txt
```

## Quickstart

### Running the scraper
```sh
python get_data.py
```

## Examples 

Now you can run Python and import the Bitfinex client.

### Public endpoints
Public endpoints can be used without providing any keys as shown in the examples below.

#### Example 1: Retrieving current tick data
```python
import bitfinex

# Initialize the api
api = bitfinex.api_v1()

# Select a trading pair
pair = 'btcusd'

# Get the current ticker data for the pair
api.ticker(pair)
```

#### Example 2: Available currency pairs
```python
import bitfinex

# Initialize the api
api = bitfinex.api_v1()

# Get all available currency pairs
symbols = api.symbols()
```

All available public endpoints are included in this client. For a full documentation check the Bitfinex API [webpage.](
https://docs.bitfinex.com/docs/public-endpoints)

### Private endpoints
In order to use private endpoints the public- and secrete keys need to be provided while initializing the API as shown in the example below in which the current account balance can be retrieved.

#### Example 1: Check account balance
```python
import bitfinex

key = 'YOUR_PUBLIC_KEY'
secrete = 'YOUR_SECRETE_KEY'

api = bitfinex.api_v1(key, secrete)
my_balance = api_bitfinex.balance()
```

#### Example 2: Place a buy order
```python
import bitfinex

symbol = 'btcusd'        # Currency pair to trade
amount = '0'             # Amount to buy
price = '0'              # Buy price
side = 'buy'             # Buy or sell
type = 'exchange market' # Which type

# Send the order
api.place_order(symbol, amount, price, side, type)
```

## Contributing

1. Fork it ( https://github.com/tuangeek/cryptocurrency-OHLC/fork )
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request

## Credits

Original git and script from [akcarsten/bitfinex_api] (https://github.com/akcarsten/bitfinex_api)
