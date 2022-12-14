import pandas as pd
from binance.client import Client
import datetime
import re
import os
from fp.fp import FreeProxy 
# get api key and secret from environment variables secret.KEY and secret.SECRET
api_key = os.environ.get('KEY',None)
api_secret = os.environ.get('SECRET',None)
use_proxy = os.environ.get('USE_PROXY',"NO")

if use_proxy == "YES":
    proxy={
        'http': FreeProxy(rand=True, timeout=1).get(),
        'https': FreeProxy(rand=True, timeout=1,https=True).get()
    }
    print(f"Using proxy: {proxy}")

if api_key is None: 
    print('API key not found in environment variables')
    client = Client()
elif api_secret is None:
    print('API secret not found in environment variables')
    client = Client()
else:
    print('API key and secret found in environment variables')
    client = Client(api_key, api_secret, requests_params={'proxies': proxy} if use_proxy == "YES" else None)


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
