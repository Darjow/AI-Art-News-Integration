from threads.abstractThread import AbstractThread
from util.volatileDictionary import VolatileDict

class HLNThread(AbstractThread):
  
  def __init__(self, volatile_dict:VolatileDict ):
    super().__init__(volatile_dict, "www.hln.be")
    
    self.routes = [
      "/buitenland/",
      "/binnenland/",
      "/vtm-nieuws/"
    ]


  def start_scraping(self): 
    print(self.limit)
    print(self.base_url)
    print(self.routes)
    
    self.append_to_dict("some")
    self.append_to_dict("thing")
    
    
    self.output_dict()