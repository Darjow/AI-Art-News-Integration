import threading
import abc
from scraper.util.volatileDictionary import VolatileDict
from datetime import datetime, time
import locale
class AbstractThread(threading.Thread, metaclass=abc.ABCMeta):
    def __init__(self, volatile_dict: VolatileDict):
        locale.setlocale(locale.LC_TIME, 'nl_NL.utf8')
        super().__init__()
        now = datetime.now()
    
        self.dict = volatile_dict
        self.limit = datetime(year=now.year, month=now.month, day=now.day, hour=0, minute=0, second=0)
        self.guard = []

        
    
    @abc.abstractmethod
    def start_scraping(self):
        pass
    
    
    def append_to_dict(self, base_url, title ): #in de toekomst: baseurl, title, likes, views, comments, ... 
        self.dict.add_result(base_url, title)
        
