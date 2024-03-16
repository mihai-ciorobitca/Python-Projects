# BinanceInfo

BinanceInfo is a Python package that provides a convenient way to retrieve Binance account information using the Binance official API. It offers features such as OTP verification using `pyotp` and returns various account details including balances.

## Installation

Install BinanceInfo from PyPI using pip:

```
pip install binance-info
```

## Usage

### Obtain API keys from Binance:

* Create an account on Binance if you haven't already.
* Navigate to the API Management section in your account settings.
* Generate a new API key with appropriate permissions (e.g., read-only).

### Set up environment variables:

You can set your Binance API key and secret as environment variables or directly pass them to the BinanceInfo functions.

### Use BinanceInfo in your Python script:

```
from binanceinfo import BinanceInfo
binance_info = BinanceInfo(api_key='your_api_key', api_secret='your_api_secret')
account_info = binance_info.get_account_info()
balances = account_info['balances']
# Display balances
for balance in balances:
    print(f"{balance['asset']}: {balance['free']} (free), {balance['locked']} (locked)")
```

## Contributing
Contributions are welcome! Feel free to open issues or pull requests for any improvements or features you'd like to add.
