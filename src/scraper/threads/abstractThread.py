import threading
from scraper.util.volatileDictionary import VolatileDict
from datetime import datetime, time
import locale
import requests
from bs4 import BeautifulSoup
import time

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
        self.articles = []
        self.visited_urls = set()
        self.remaining_articles = 0
        
        super().__init__()

    def append_to_dict(self, base_url, title):
        self.dict.add_result(base_url, title)

    def start_scraping(self):
        self.on_start()
        while True:
            print(f"[{type(self).__name__}]: {self.remaining_articles} articles remaining. Found: {len(self.articles)}")
            articles = self.get_articles()
            if not articles or len(self.articles) >= 20:
                break
            self.remaining_articles += len(articles)
            for article in articles:
                if self.should_scrape_article(article):
                    self.scrape_article(article)
                    self.remaining_articles -= 1

    def get_articles(self):
        response = requests.get(self.base_url, headers=self.headers)
        bs = BeautifulSoup(response.text, "html.parser")
        return bs.find_all("article")

    def should_scrape_article(self, article):
        a_href = article.find(name="a")
        if a_href is None:
            return False

        if a_href["href"].startswith("/"):
            article_url = self.base_url + a_href["href"]
        else:
            article_url = a_href["href"]

        if any(route in article_url for route in self.routes):
            article_date = self.get_article_date(article)
            return article_date == self.target_date and article_url not in self.visited_urls

        return False

    def get_article_date(self, article):
        date_element = article.find(self.time_tag, class_=self.time_class)
        if date_element is None:
            return None
        date_str = date_element.get("datetime")
        return datetime.strptime(date_str, self.dateformat).date()

    def scrape_article(self, article):
        a_href = article.find(name="a")
        if a_href is None:
            return
        article_url = a_href["href"]
        response = requests.get(article_url, headers=self.headers)
        bs = BeautifulSoup(response.text, "html.parser")

        page_articles = bs.find_all("article")
        for page_article in page_articles:
            page_article_url = page_article.find("a")["href"]
            if page_article_url.startswith("/"):
                page_article_url = self.base_url + page_article_url
            if page_article_url.startswith(self.base_url) and page_article_url not in self.visited_urls:
                self.articles.append(page_article)
                self.visited_urls.add(page_article_url)

        title = bs.find(self.title_tag, class_=self.title_class)
        if title is not None:
            self.append_to_dict(article_url, title.text.strip())

    def on_start(self):
        print(f"[{type(self).__name__}]: Starting scraper...")
