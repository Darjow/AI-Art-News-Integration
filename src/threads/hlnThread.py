import threading
from util.volatileDictionary import VolatileDict

class HLNThread(threading.Thread):
  
  def __init__(self, volatile_dict:VolatileDict ):
    super().__init__()
    self.volatile_dict = volatile_dict

  def start_scraping(self): 
    result = "some result"
    print(result)
    self.volatile_dict.add_result(self.name, result)