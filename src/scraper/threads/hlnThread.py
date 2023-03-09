from scraper.threads.abstractThread import AbstractThread
from scraper.util.volatileDictionary import VolatileDict
from bs4 import BeautifulSoup
import requests
from datetime import datetime

class HLNThread(AbstractThread):

  def __init__(self, volatile_dict:VolatileDict):
    super().__init__(volatile_dict, "%d %B %Y %H:%M", "article__title", "article__time", "https://www.hln.be")
    self.routes = [
      "/buitenland/",
      "/binnenland/",
      "/vtm-nieuws/"
    ]
    self.articles = []

  def get_articles(self):
    if not self.articles:
      self.articles.append(self.base_url)
      current = self.articles.pop(0)
      response = requests.get(current, headers=self.headers)
      bs = BeautifulSoup(response.text, "html.parser")
      articles = bs.find_all("article")
      return articles

  def should_scrape_article(self, article):
    should_scrape = super().should_scrape_article(article)
    if not should_scrape:
      return False
      route = article.find("a").get("href")
      return any(route.startswith(r) for r in self.routes)

  def scrape_article(self, article):
    title = article.find("h3", class_=self.title_class)
    if title is not None:
      self.append_to_dict(self.base_url + article.find("a").get("href"), title.text.strip())
