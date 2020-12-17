import time
from datetime import datetime, timedelta

import requests


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
