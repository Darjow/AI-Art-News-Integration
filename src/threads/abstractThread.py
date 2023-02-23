import threading
import abc
from util.volatileDictionary import VolatileDict
from datetime import datetime, time

class AbstractThread(threading.Thread, metaclass=abc.ABCMeta):
    def __init__(self, volatile_dict: VolatileDict):
        super().__init__()
        now = datetime.now()
    
        self.dict = volatile_dict
        self.limit = datetime(year=now.year, month=now.month, day=now.day, hour=0, minute=0, second=0)
        self.guard = []

        
    
    @abc.abstractmethod
    def start_scraping(self):
        pass
    
    
    def append_to_dict(self, base_url, item ): #in de toekomst: baseurl, title, likes, views, comments, ... 
        self.dict.add_result(base_url, item)
        
    def output_dict(self):
        print(self.dict.get_dict())