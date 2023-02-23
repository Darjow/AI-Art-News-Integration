import threading
import abc
from util.volatileDictionary import VolatileDict

class AbstractThread(threading.Thread, metaclass=abc.ABCMeta):
    def __init__(self, volatile_dict: VolatileDict):
        super().__init__()
        self.volatile_dict = volatile_dict
        
    
    @abc.abstractmethod
    def start_scraping(self):
        pass
    