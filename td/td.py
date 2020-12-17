import time
import pytz
import configparser
from datetime import datetime, timedelta
import requests

conf = configparser.ConfigParser()
conf.read("data/conf.ini")


# Call the td ameritrade hours endpoint for equities to see if it is open
def marketOpen():
  """
  Return True or False if stock market was open today
  """
  tz          = conf['GLOBAL']['timezone']
  today       = datetime.today().astimezone(pytz.timezone(tz))
  today_fmt   = today.strftime('%Y-%m-%d')
  tdHoursURL  = conf['TD']['hoursURL']
  key         = conf['TD']['key']
  params = {
    'apikey': key,
    'date': today_fmt
    }

  request = requests.get(
    url=tdHoursURL,
    params=params
    ).json()
  
  
  if request['equity']['EQ']['isOpen'] is True:
    return(True)
  else:
    return(False)


# The TD Ameritrade api has a limit to the number of symbols you can get data for
# in a single call so this function breaks the tlist (ticker list) up into 'n' length chunks 
def chunks(tlist, n):
  """
  Takes in a list and how long you want
  each chunk to be
  """
  n = max(1, n)
  return (tlist[i:i+n] for i in range(0, len(tlist), n))


def quotes_request(ticker, api_key, params):
  """
  Makes an api call for a list of stock symbols
  and returns a dataframe
  """
  url = r"https://api.tdameritrade.com/v1/marketdata/quotes"

  params = {
  'apikey': api_key,
  'symbol': stocks
  }

  request = requests.get(
    url=url,
    params=params
    ).json()

  time.sleep(1)

  return pd.DataFrame.from_dict(
    request,
    orient='index'
    ).reset_index(drop=True)
