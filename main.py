import pytz
import configparser
import eodata
import td
import json
from datetime import datetime, timedelta

# Set configuration
confFile = "data/conf.ini"  
conf = configparser.ConfigParser()
conf.read(confFile)


if __name__ == "__main__":
  tickers = eodata.loadTickers(confFile)
  if td.marketOpen():
    print("Market Open!")
  else:
    print("Market Closed...")