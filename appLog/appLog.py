import configparser
import logging

# Set configuration
confFile = "data/conf.ini"  
conf = configparser.ConfigParser()
conf.read(confFile)
dataDir = conf['GLOBAL']['dataDir']

# Set up logging params
logLevel  = conf['GLOBAL']['logLevel']
logFile   = dataDir + conf['GLOBAL']['logFile']

appLog = logging
appLog.basicConfig(
    filename=logFile,
    level=logLevel,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
