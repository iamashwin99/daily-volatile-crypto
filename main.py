import pandas as pd
from binance.client import Client
import datetime
import re
import os

# get api key and secret from environment variables secret.KEY and secret.SECRET
api_key = os.environ.get('secrets.KEY',None)
api_secret = os.environ.get('secrets.SECRET',None)

if api_key is None or api_secret is None:
    print('API key or secret not found in environment variables')
    client = Client()
else:
    print('API key and secret found in environment variables')
    client = Client(api_key, api_secret)


client = Client()
date_time =datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
print(f"getting data on {date_time}")

def getMeans(ticker):
    klines = client.get_historical_klines(ticker, Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
    df = pd.DataFrame(klines)
    df['per'] = abs(df[4].astype(float) - df[1].astype(float) )*100 /df[1].astype(float)
    return df.per.mean()

# import ticker data for all binance instruments in 1 day period
ticker_data2 = client.get_ticker()
symbols=pd.DataFrame(ticker_data2)['symbol']
list=[]
for symbol in symbols:
  if(re.search("USDT", symbol)) :
      try:
          list.append([ symbol , getMeans(symbol)])
      except:
          continue

list=pd.DataFrame(list,columns=['symbol','per'])



list.to_csv(date_time)
