from scraper.threads.abstractThread import AbstractThread
from scraper.util.volatileDictionary import VolatileDict
from bs4 import BeautifulSoup
import requests

class DeMorgenThread(AbstractThread):
  def __init__(self, volatile_dict: VolatileDict):
    super().__init__(volatile_dict, "%d %B %Y", "p", "artstyle__intro", "time","artstyle__production__datetime", "https://www.demorgen.be", [])

  
  def on_start(self):
    super().on_start()
    response = requests.get(self.base_url, headers = self.headers)
    bs = BeautifulSoup(response.text, "html.parser")
    nav = bs.find_all("a", attrs={"class", "app-navigation__link"})
    self.routes = [i["href"] for i in nav]
    self.routes.append("/nieuws")
    self.routes.append("/snelnieuws")