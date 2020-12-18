import pytz
import configparser
import eodata
import td
import pandas as pd
import json
from appLog import appLog
import sys
from datetime import datetime, timedelta

# Set configuration
confFile = "data/conf.ini"  
conf = configparser.ConfigParser()
conf.read(confFile)
dataDir = conf['GLOBAL']['dataDir']


def formatBqTable(data):
  pass


def writeCSV(data):
  """
  pass in a dataframe, function writes to csv file defined
  in data/conf.ini under ['GLOBAL']['quotesCSV']
  """
  quoteFile = conf['GLOBAL']['dataDir'] + conf['GLOBAL']['quotesCSV']
  try:
    data.to_csv(quoteFile, index=False)
    message = "\'{}\' written sucessfully".format(quoteFile)
    appLog.info(message)
  except:
    message = "Write failed! File \'{}\' is not writable".format(quoteFile)
    appLog.error(message)
    sys.exit(message + "\nExiting now")



if __name__ == "__main__":
  tickers = eodata.loadTickers(confFile)
  sortedTicks = tickers.sort()
  if td.marketOpen():
    appLog.info("Market Open! Starting quote runner...")
    pass
  else:
    appLog.info("Market Closed... Not running")
    exit(0)

  chunks = list(td.chunks(list(set(tickers)), 2))   # break the tickers into chunks to comply with td's rate limiting
  appLog.info("There are %d tickers to analyze" % (len(chunks[0])))  
  appLog.info("list of chunks: {}".format(chunks[0]))

  data = pd.concat([td.quotes_request(each) for each in chunks[0]])

  if writeCSV(data):
    appLog.info("Runner finished sucessfully!")
    pass
  
  
  
  