from scraper.util.volatileDictionary import VolatileDict
from scraper.threads.abstractThread import AbstractThread
from scraper.threads.hlnThread import HLNThread
from scraper.threads.deMorgenThread import DeMorgenThread
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

class Scraper:
  def __init__(self):
    self.threads: List[AbstractThread] = []
    self.dict = VolatileDict()
    
    scraping_date = datetime(2022, 12, 1)
    
    self.threads.append(HLNThread(self.dict, scraping_date))
    self.threads.append(DeMorgenThread(self.dict, scraping_date))

  def start_scraping(self):    
    with ThreadPoolExecutor() as pool:
      futures = [pool.submit(thread.start_scraping) for thread in self.threads]

    for future in futures:
      future.result()

    return self.dict.output_dict()