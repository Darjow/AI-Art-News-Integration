import threading
from scraper.util.volatileDictionary import VolatileDict
from datetime import datetime, time
import locale
import requests
from bs4 import BeautifulSoup
import time
class AbstractThread(threading.Thread):
  def __init__(self, volatile_dict: VolatileDict, dateformat: str, title_tag: str, title_class: str, time_tag: str, time_class: str, base_url: str, routes: []):
    
    #Stelt taal in op nederlands zodat de datums gemakkelijk gescraped kunnen worden. 
    locale.setlocale(locale.LC_TIME, 'nl_NL.utf8')
        
    #De thread safe dictionary wordt verwerkt.
    self.dict = volatile_dict
    
    #Variabele die huidige tijd opslaat.    
    now = datetime.now()
    
    #Stelt het maximum waarde in waarvan de artikels ouder moeten zijn.
    self.limit = datetime(year=now.year, month=now.month, day=now.day, hour=0, minute=0, second=0)
    
    #Lijst van artikels die moeten geprocessed worden. 
    self.articles = []
    
    #Het formaat van de datum die op een artikel voorkomt wordt ingesteld.
    self.dateformat = dateformat
    
    #De klasses waar de data in voorkomt. 
    self.title_tag = title_tag
    self.title_class = title_class
    self.time_tag = time_tag
    self.time_class = time_class
    
    #De url waarop de scraper moet starten.
    self.base_url = base_url
    
    #De verschillende routes waarop de scraper mag scrapen. Rekening houdend met robots.txt. 
    self.routes = routes
    
    #De headers die nodig zijn om toegang te hebben tot de website.
    self.headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
      "Accept-Encoding": "gzip, deflate, br",
      "Accept-Language": "nl-NL,nl;q=0.8",
      "Cache-Control": "max-age=0",
      "Cookie":"authId=84f9c58f-0da1-4752-a294-74df52a18ec8;",
    }
    
    #Thread klasse wordt geïnitialiseerd. 
    super().__init__()

    #Artikel die werd gevonden door de scraper en als actief wordt gezet.
    self.current = None
    
    #Link van de self.current die voorkomt in de self.routes en momenteel gescraped (zal) word(t)(en).
    self.article_link = None

  def append_to_dict(self, base_url, title ):
    self.dict.add_result(base_url, title)
    
  def start_scraping(self):
    self.on_start()    
    while len(self.articles) > 0:
      print(f"[{type(self).__name__}]: {len(self.articles)} to process")
      self.current = self.articles.pop()
      if self.should_scrape_article(self.current):
        self.scrape_article()
          

  def should_scrape_article(self, article):
    a_href = article.find(name="a")
    temp = None

    if a_href == None:
      return False
  

    if a_href["href"].startswith("/"):
      temp = self.base_url + a_href["href"]
    
    if temp != None:
      if any(route in temp for route in self.routes):
        self.article_link = temp
        return True
      
    if any(route in a_href.get('href', '') for route in self.routes):
      self.article_link = a_href["href"]
      return True   


  def scrape_article(self):
    response = requests.get(self.article_link, headers=self.headers)
    bs = BeautifulSoup(response.text, "html.parser")
    date = bs.find(self.time_tag, class_= self.time_class)    
    title = bs.find(self.title_tag, class_ =self.title_class)

    time.sleep(50/1000)

    if date is None:
      return
    
    if title is None:
      return
    
    date_obj = date["datetime"]
    try:
      date_time_obj = datetime.strptime(date_obj, self.dateformat)
      if date_time_obj >= self.limit:
        self.append_to_dict(self.base_url,title.text.strip())
    except(ValueError):
      return
    

  def on_start(self):
    response = requests.get(self.base_url, headers = self.headers)
    bs = BeautifulSoup(response.text, "html.parser")
    self.articles = bs.find_all("article")[:20]
        
