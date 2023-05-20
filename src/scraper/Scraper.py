from scraper.util.volatileDictionary import VolatileDict
from scraper.threads.abstractThread import AbstractThread
from scraper.threads.hlnThread import HLNThread
from scraper.threads.deMorgenThread import DeMorgenThread
from concurrent.futures import ThreadPoolExecutor


class Scraper:
  def __init__(self):
    self.threads: List[AbstractThread] = []
    self.dict = VolatileDict()
    
    self.threads.append(HLNThread(self.dict))
    self.threads.append(DeMorgenThread(self.dict))

  def start_scraping(self):    
    with ThreadPoolExecutor() as pool:
      futures = [pool.submit(thread.start_scraping) for thread in self.threads]

    for future in futures:
      future.result()

    return self.dict.output_dict()