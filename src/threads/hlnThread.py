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
    
    self.guard = []
    


  def start_scraping(self): 
    self.articles.append(f"{self.base_url}{self.routes[0]}")
    
    while len(self.articles) > 0:
      print(f"{len(self.articles)} to process")
      current = self.articles.pop()
      
      response = requests.get(current)
      bs = BeautifulSoup(response.text, "html.parser")
      articles = bs.find_all("article")
      for article in articles:
        self.add_article(article)
        title_element = article.find("h2", class_='title')
        if title_element:
          title = title_element.text.strip()
          self.append_to_dict(current, title)
      
      
  def add_article(self, article: str):
    if self.guard.count(article) > 0:
      return
    
    self.guard.append(article)
    self.articles.append(article)
    print(f"Found new article: {article}")