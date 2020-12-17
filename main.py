import configparser

# Get configuration
conf = configparser.ConfigParser()
conf.read('data/conf.ini')

print(conf['ALPACA']['key_id'])