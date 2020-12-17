import pytz
import configparser
import eodata
import os.path
from os import path
import json
from datetime import datetime, timedelta

# Get configuration
conf = configparser.ConfigParser()
conf.read('data/conf.ini')

# Set constants from config
timezone        = conf['GLOBAL']['timezone']
createTickFile  = conf['GLOBAL']['createTickFile']
dataDir         = conf['GLOBAL']['dataDir']
tickFile        = dataDir + conf['GLOBAL']['tickFile']

# Load ticker file if present, otherwise call func to retrieve
# Pass True to create file data/tickers.json with a list of tickers and a dict containing "tickers":"company name"
# Pass False to only return a list of tickers

if path.exists(tickFile):
    print("found tickers.json, loading file")
    with open(tickFile) as f:
      tickers = json.load(f)
      tickers = tickers['tickers']
else:
    if createTickFile:
      print("tickers.json not found, populating")
      tickers = eodata.populateTickers(dataDir, True)
    else:
      print("createTickFile false, only returning tickers")
      tickers = eodata.populateTickers(dataDir, False)




today = datetime.today().astimezone(pytz.timezone(timezone))
today_fmt = today.strftime('%Y-%m-%d')

# Call the td ameritrade hours endpoint for equities to see if it is open
market_url = 'https://api.tdameritrade.com/v1/marketdata/EQUITY/hours'

params = {
    'apikey': api_key,
    'date': today_fmt
    }

request = requests.get(
    url=market_url,
    params=params
    ).json()