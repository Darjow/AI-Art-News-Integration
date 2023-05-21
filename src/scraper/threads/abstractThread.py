import threading
from scraper.util.volatileDictionary import VolatileDict
from datetime import datetime, time
import locale
import requests
from bs4 import BeautifulSoup
import time
import dateparser

class AbstractThread(threading.Thread):
  def __init__(self, volatile_dict: VolatileDict, dateformat: str, title_tag: str, title_class: str, time_tag: str, time_class: str, base_url: str, routes: [], target_date: datetime):
    locale.setlocale(locale.LC_TIME, 'nl_NL.utf8')
    self.dict = volatile_dict
    self.dateformat = dateformat
    self.title_tag = title_tag
    self.title_class = title_class
    self.time_tag = time_tag
    self.time_class = time_class
    self.base_url = base_url
    self.routes = routes
    self.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "nl-NL,nl;q=0.8",
        "Cache-Control": "max-age=0",
        "Cookie": "authId=84f9c58f-0da1-4752-a294-74df52a18ec8;",
    }
    self.target_date = target_date
    self.urls = []
    self.visited_urls = set()
    self.found = 0

    super().__init__()

  def append_to_dict(self, base_url, title):
    self.dict.add_result(base_url, title)

  def start_scraping(self):
    self.on_start()

    while len(self.urls) > 0 and self.found < 20:
      print(f"[{type(self).__name__}]: {len(self.urls)} URLs remaining. Found: {self.found}")
      url = self.urls.pop()

      if self.should_scrape_url(url):
        self.scrape_url(url)
        self.visited_urls.add(url)

  def should_scrape_url(self, url):
    if url in self.visited_urls:
      return False
      
    if url.startswith("/"):
      url = self.base_url + url

    if any(route in url for route in self.routes):
      return True

    return False

  def scrape_url(self, url):
    if url.startswith("/"):
      url = self.base_url + url
      
    response = requests.get(url, headers=self.headers)
    bs = BeautifulSoup(response.text, "html.parser")

    page_urls = [a.get("href") for a in bs.find_all("a")]
    
    for page_url in page_urls:
      if self.should_scrape_url(page_url):
        self.urls.append(page_url)

    title = bs.find(self.title_tag, class_=self.title_class)
    date = bs.find(self.time_tag, class_= self.time_class)
        
    if title is not None and date is not None:
      date_obj = date["datetime"]
      if date_obj is not None:
        date_time_obj = dateparser.parse(date_obj)
        if date_time_obj.date() == self.target_date.date():
          self.append_to_dict(url, title.text.strip())
          self.found += 1

  def on_start(self):
    print(f"[{type(self).__name__}]: Starting scraper...")
    self.scrape_url(self.base_url)