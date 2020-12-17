import pytz
import configparser
import eodata
import td
import os.path
from os import path
import json
from datetime import datetime, timedelta

# Get configuration
conf = configparser.ConfigParser()
conf.read('data/conf.ini')          # unfortunately don't see a way around hardcoding this value

# Set constants from config
timezone        = conf['GLOBAL']['timezone']
createTickFile  = conf['GLOBAL']['createTickFile']
dataDir         = conf['GLOBAL']['dataDir']
tickFile        = dataDir + conf['GLOBAL']['tickFile']

# Load ticker file if present, otherwise call func to retrieve
# Pass True to create file data/tickers.json with a list of tickers and a dict containing "tickers":"company name"
# Pass False to only return a list of tickers

def loadTickers():
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
    return(tickers)

if __name__ == "__main__":
    tickers = loadTickers()
    if td.marketOpen():
      print("Market Open!")
    else:
      print("Market Closed...")