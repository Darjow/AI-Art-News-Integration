import threading
from datetime import datetime, time
import locale
import requests
from bs4 import BeautifulSoup
import time
from requests_html import HTMLSession

class StandaardScraper(threading.Thread):
  def __init__(self, date: datetime):
    
    locale.setlocale(locale.LC_TIME, 'nl_NL.utf8')
      
    self.dict = []
        
    self.url  = f"https://www.standaard.be/archief/cnt/{date.year}/{date.month}/{date.day}"
    self.date = date
        
    self.headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
      "Accept-Encoding": "gzip, deflate, br",
      "Accept-Language": "nl-NL,nl;q=0.8",
      "Cache-Control": "max-age=0",
      "Cookie":"authId=84f9c58f-0da1-4752-a294-74df52a18ec8;",
    }
    
    super().__init__()
    
  def start_scraping(self):
    bs = self.on_start()
    
    articles = bs.find_all("section", attrs={"class": "l-zone"})
    for article in articles:
      for ul in article.find_all("ul"):
        for li in ul.find_all("li"):
          if len(self.dict) == 100: #Geen maximum content. 
            break
          
          self.dict.append(li.get_text(strip=True))
          
    return self.dict
        
  def on_start(self):
    session = HTMLSession()
    response = session.get(self.url)
    response.html.render()
    return BeautifulSoup(response.html.html, "html.parser")
