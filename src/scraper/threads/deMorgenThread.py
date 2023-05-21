from scraper.threads.abstractThread import AbstractThread
from scraper.util.volatileDictionary import VolatileDict
from bs4 import BeautifulSoup
import requests
from datetime import datetime

class DeMorgenThread(AbstractThread):
  def __init__(self, volatile_dict: VolatileDict, date: datetime):    
    super().__init__(volatile_dict, "%d %B %Y", "h1", "artstyle__header-title", "time","artstyle__production__datetime", "https://www.demorgen.be", [], date)

  
  def on_start(self):
    response = requests.get(self.base_url, headers = self.headers)
    bs = BeautifulSoup(response.text, "html.parser")
    nav = bs.find_all("a", attrs={"class", "app-navigation__link"})
    self.routes = [self.base_url + i["href"] for i in nav]
    self.routes.append(self.base_url + "/nieuws")
    self.routes.append(self.base_url + "/snelnieuws")
    
    super().on_start()

