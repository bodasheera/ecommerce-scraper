import os
from scrapy.cmdline import execute
import json


os.chdir(os.path.dirname(os.path.realpath(__file__)))
print(os.getcwd())

import pandas as pd

from db import flipkart
from orchestrator import Orchestrator

start_urls = ['https://www.flipkart.com/search?q=mobile&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off']


orc = Orchestrator(flipkart)
#orc.trigger_specific_level_scraping(config_id = 1, start_urls = start_urls, extra_config = None)
# orc.trigger_specific_level_scraping(2,start_urls=[], extra_config=None)
orc.trigger_specific_level_scraping(3,start_urls=[], extra_config=None)