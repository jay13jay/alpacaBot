import string
import configparser
import requests
import json
from bs4 import BeautifulSoup


# eodata stores the tickers based on the first letter
# for example: AAPL - Apple will be stored on  http://eoddata.com/stocklist/NYSE/A.htm


# Create list of all letteres to iterate over eodata pages
def populateTickers(confDir, wbool):
    conf = configparser.ConfigParser()
    conf.read(confDir+"conf.ini")
    baseURL = conf['EODATA']['base_url']
    alpha = list(string.ascii_uppercase)
    symbols = []
    data = {}
    data['tickers'] = []    

    for page in alpha:
        url = baseURL + page + '.htm'
        resp = requests.get(url)
        site = resp.content
        soup = BeautifulSoup(site, 'html.parser')
        table = soup.find('table', {'class': 'quotes'})
        for row in table.findAll('tr')[1:]:
            tick = row.findAll('td')[0].text.rstrip()   # get ticker symbol
            tick = tick.replace(".", "-")               # replace . to make cleaning easier
            tick = tick.split('-')[0]                   # clean symbols of trailing chars
            tickName = row.findAll('td')[1].text.rstrip()   # get company name from ticker
            symbols.append(tick)
            data['tickers'].append(tick)
            data[tick] = tickName
    # check wbool, if true, write file, either way, return tickers
    if wbool:    
        with open(confDir + 'tickers.json', 'w') as f:
            json.dump(data, f)

    return(data['tickers'])