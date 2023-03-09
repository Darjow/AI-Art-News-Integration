import threading
import abc
from scraper.util.volatileDictionary import VolatileDict
from datetime import datetime, time
import locale
import requests
from bs4 import BeautifulSoup

class AbstractThread(threading.Thread, metaclass=abc.ABCMeta):
  def __init__(self, volatile_dict: VolatileDict, dateformat: str, title_class: str, time_class: str, base_url: str):
    locale.setlocale(locale.LC_TIME, 'nl_NL.utf8')
    now = datetime.now()
    self.dict = volatile_dict
    self.limit = datetime(year=now.year, month=now.month, day=now.day, hour=0, minute=0, second=0)
    self.guard = []
    self.dateformat = dateformat
    self.title_class = title_class
    self.time_class = time_class
    self.base_url = base_url
    super().__init__()
    self.headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
      "Accept-Encoding": "gzip, deflate, br",
      "Accept-Language": "nl-NL,nl;q=0.8",
      "Cache-Control": "max-age=0",
      "Cookie":"authId=84f9c58f-0da1-4752-a294-74df52a18ec8;",
    }
    

  def append_to_dict(self, base_url, title ):
    self.dict.add_result(base_url, title)
    
  def start_scraping(self):
    self.on_start()
    while True:
      articles = self.get_articles()
      if not articles:
        break
      for article in articles:
        if self.should_scrape_article(article):
          self.scrape_article(article)

  def should_scrape_article(self, article):
    date = article.find(name="time", attrs={"class": self.time_class}).get("datetime")
    date_time_obj = datetime.strptime(date, self.dateformat)
    return date_time_obj >= self.limit

  def scrape_article(self, article):
    title = article.find(name="p", attrs={"class": self.title_class})
    if title is not None:
      self.append_to_dict(self.base_url, title.text.strip())

  def on_start(self):
    print(self.base_url)
    response = requests.get(self.base_url, headers = self.headers)
    bs = BeautifulSoup(response.text, "html.parser")
    articles = bs.find_all("article")
    time = bs.find_all(name="time", attrs={"class", "article__time"})
    title = bs.find_all(name="h1", attrs={"class", "article__title"})
        
