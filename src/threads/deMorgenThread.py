from threads.abstractThread import AbstractThread
from util.volatileDictionary import VolatileDict
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime

class DeMorgenThread(AbstractThread):
  
  def __init__(self, volatile_dict:VolatileDict ):
    super().__init__(volatile_dict)
    
    self.routes = []
    self.base_url = "https://www.demorgen.be"
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
    self.on_start()
    
    self.articles.append(f"{self.base_url}{self.routes[0]}")
    
    while len(self.articles) > 0:
      print(f"[{type(self).__name__}]: {len(self.articles)} to process")
      current = self.articles.pop()
      response = requests.get(current, headers = self.headers)
                  
      
      bs = BeautifulSoup(response.text, "html.parser")
      articles = bs.find_all("article")
      time = bs.find_all(name="time", attrs={"class", "artstyle__production__datetime"})
      title = bs.find_all(name="p", attrs={"class", "artstyle__intro"})
      
      
      if len(time) == 1:
        date = time[0]["datetime"]
        date_format = "%d %B %Y"
        date_time_obj = datetime.strptime(date, date_format)
        if date_time_obj >= self.limit:
          if len(title) == 1:
            self.append_to_dict(self.base_url, title[0].text)
            
                                    
      for article in articles:
        first = article.findChild()
        a_href = article.findChildren()[1]
        if first == None:
          continue
        if first.name != "div":
          if first.name != "hr":
            continue
        if a_href.name != "a":
          continue        
        if any(route in a_href.get('href', '') for route in self.routes):
          self.add_article(self.base_url + a_href["href"])        
    
    

        
      
  def add_article(self, article: str):
    if self.guard.count(article) > 0:
      return
  
    self.guard.append(article)
    self.articles.append(article)
    
    
  def on_start(self):
    response = requests.get(self.base_url, headers = self.headers)
    bs = BeautifulSoup(response.text, "html.parser")
    nav = bs.find_all("a", attrs={"class", "app-navigation__link"})
    
    self.routes = [i["href"] for i in nav]
