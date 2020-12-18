from distutils.core import setup
import setuptools
import py2exe
import pytz
import time
import configparser
import requests
import pandas as pd
from datetime import datetime, timedelta
from appLog import appLog
import pytz.lazy
 
setup(console=['main.py'])