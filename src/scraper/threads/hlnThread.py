from scraper.threads.abstractThread import AbstractThread
from scraper.util.volatileDictionary import VolatileDict
from datetime import datetime

class HLNThread(AbstractThread):

  def __init__(self, volatile_dict:VolatileDict, date: datetime):
    super().__init__(volatile_dict, "%d-%m-%y, %H:%M", "h1","article__title", "time","article__time", "https://www.hln.be", ["/buitenland/","/binnenland/","/vtm-nieuws/"], date)

