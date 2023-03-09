from scraper.threads.abstractThread import AbstractThread
from scraper.util.volatileDictionary import VolatileDict
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime

class DeMorgenThread(AbstractThread):
  def __init__(self, volatile_dict: VolatileDict):
    super().__init__(volatile_dict, "%d %B %Y", "artstyle__intro", "artstyle__production__datetime", "https://www.demorgen.be")
    self.routes = []

    self.articles = []

  def get_articles(self):
    if not self.articles:
      self.articles.append(f"{self.base_url}")
    current = self.articles.pop(0)
    response = requests.get(current, headers=self.headers)
    bs = BeautifulSoup(response.text, "html.parser")
    articles = bs.find_all("article")
    return articles

  def should_scrape_article(self, article):
    should_scrape = super().should_scrape_article(article)
    if not should_scrape:
      return False
    route = article.find(name="a").get("href")
    return any(route.startswith(r) for r in self.routes)

  def add_article(self, article: str):
    if article in self.guard:
      return
    self.guard.append(article)
    self.articles.append(article)
    
  
  def on_start(self):
    super().on_start()
    response = requests.get(self.base_url, headers = self.headers)
    bs = BeautifulSoup(response.text, "html.parser")
    nav = bs.find_all("a", attrs={"class", "app-navigation__link"})
    self.routes = [i["href"] for i in nav]
    self.routes.append("/nieuws")
    self.routes.append("/snelnieuws")