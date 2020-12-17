import configparser
import eodata

# Get configuration
conf = configparser.ConfigParser()
conf.read('data/conf.ini')
# print(conf['ALPACA']['key_id'])

# Set constants from config
baseURL = conf['ALPACA']['endpoint']
keyID = conf['ALPACA']['key_id']
secretKey = conf['ALPACA']['secret_key']


tickers = eodata.populateTickers('data/', True)