import string
import configparser
import requests
import json
from bs4 import BeautifulSoup


# Setup constants
conf = configparser.ConfigParser()
conf.read('../data/conf.ini')
baseURL = conf['EODATA']['base_url']


# eodata stores the tickers based on the first letter
# for example: AAPL - Apple will be stored on  http://eoddata.com/stocklist/NYSE/A.htm



# Create list of all letteres to iterate over eodata pages
def getTickers():
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
        
    print(data['tickers'])
    with open('../data/tickers.json', 'w') as f:
        json.dump(data, f)
        


if __name__ == "__main__":
    getTickers()