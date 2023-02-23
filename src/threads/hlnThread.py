from threads.abstractThread import AbstractThread
from util.volatileDictionary import VolatileDict
from bs4 import BeautifulSoup
import requests
import time
class HLNThread(AbstractThread):
  
  def __init__(self, volatile_dict:VolatileDict ):
    super().__init__(volatile_dict)
    
    self.routes = [
      "/buitenland/",
      "/binnenland/",
      "/vtm-nieuws/"
    ]
    self.base_url = "https://www.hln.be"
    self.articles = []
    


  def start_scraping(self): 
    self.articles.append(f"{self.base_url}{self.routes[0]}")
    
    while len(self.articles) > 0:
      print(f"{len(self.articles)} to process")
      current = self.articles.pop()
      
      response = requests.get(current)
  
      bs = BeautifulSoup(response.text, "html.parser")
      time.sleep(2)
      print(response.text)
      articles = bs.find_all("article")
      for article in articles:
        title_element = article.find("h2", class_='title')
        if title_element:
          title = title_element.text.strip()
          print(title)
      
      
