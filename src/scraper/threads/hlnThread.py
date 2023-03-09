from scraper.threads.abstractThread import AbstractThread
from scraper.util.volatileDictionary import VolatileDict
from bs4 import BeautifulSoup
import requests
from datetime import datetime

class HLNThread(AbstractThread):

  def __init__(self, volatile_dict:VolatileDict):
    super().__init__(volatile_dict, "%d %B %Y %H:%M", "h1","article__title", "time","article__time", "https://www.hln.be", ["/buitenland/","/binnenland/","/vtm-nieuws/"])

