import string
import configparser
import requests
import json
import os.path
from os import path
from bs4 import BeautifulSoup


def loadTickers(confFile):
    """
    Load ticker file if present, otherwise call func to retrieve
    Pass True to create file data/tickers.json with a list of tickers and a dict containing "tickers":"company name"
    Pass False to only return a list of tickers
    """
    # Set the variables from the config file
    conf = configparser.ConfigParser()
    conf.read(confFile)
    dataDir = conf['GLOBAL']['dataDir']
    tickFile = dataDir + conf['GLOBAL']['tickFile']
    createTickFile = conf['GLOBAL']['createTickFile']
    baseURL = conf['EODATA']['base_url']

    if path.exists(tickFile):
        print("found tickers.json, loading file")
        with open(tickFile) as f:
            tickers = json.load(f)
            tickers = tickers['tickers']
    else:
        if createTickFile:
            print("tickers.json not found, populating")
            tickers = populateTickers(True, baseURL, tickFile)
        else:
            print("createTickFile false, only returning tickers")
            tickers = populateTickers(False, baseURL, tickFile)
    return(tickers)

# Create list of all letteres to iterate over eodata pages
def populateTickers(wbool, baseURL, tickFile): 
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
        with open(tickFile, 'w') as f:
            json.dump(data, f)

    return(data['tickers'])