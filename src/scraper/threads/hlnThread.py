from scraper.threads.abstractThread import AbstractThread
from scraper.util.volatileDictionary import VolatileDict
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime

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
    self.headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
      "Accept-Encoding": "gzip, deflate, br",
      "Accept-Language": "nl-NL,nl;q=0.8",
      "Cache-Control": "max-age=0",
      "Cookie":"authId=84f9c58f-0da1-4752-a294-74df52a18ec8;",
    }
    
    


  def start_scraping(self): 
    self.articles.append(f"{self.base_url}")
    
    while len(self.articles) > 0:
      print(f"[{type(self).__name__}]: {len(self.articles)} to process")
      current = self.articles.pop()
      response = requests.get(current, headers = self.headers)
      bs = BeautifulSoup(response.text, "html.parser")
      articles = bs.find_all("article")
      time = bs.find_all(name="time", attrs={"class", "article__time"})
      title = bs.find_all(name="h1", attrs={"class", "article__title"})
      
      if len(time) == 1:
        date = time[0]["datetime"]
        date_format = "%d-%m-%y, %H:%M"
        try:
          date_time_obj = datetime.strptime(date, date_format)
          if date_time_obj >= self.limit:
            if len(title) == 1:
              self.append_to_dict(self.base_url, title[0].text)          
        except(ValueError):
          continue

      
            
      for article in articles:
        first = article.findChild()
        if first == None:
          continue
        if first.name != "a":
          continue
        if any(route in first.get('href', '') for route in self.routes):
          self.add_article(first["href"])         
    
    

        
      
  def add_article(self, article: str):
    if self.guard.count(article) > 0:
      return
    
    self.guard.append(article)
    self.articles.append(article)
    
    
    