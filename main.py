from alpaca.trading.client import TradingClient
from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import StockBarsRequest


from configparser import ConfigParser

config = ConfigParser()

config.read('config.ini')

api_key = config.get('alpaca', 'api_key')
secret_key = config.get('alpaca', 'secret_key')

agent = TradingClient(api_key, secret_key, paper=True)

account = agent.get_account()

stock = StockBarsRequest(symbol_or_symbols=["TQQQ"],
                         timeframe=TimeFrame.Minute())

print(stock)
















