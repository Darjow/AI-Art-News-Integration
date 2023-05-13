from scraper.threads.hlnThread import HLNThread
from scraper.threads.deMorgenThread import DeMorgenThread
from scraper.util.volatileDictionary import VolatileDict
from scraper.threads.abstractThread import AbstractThread
from typing import List
from concurrent.futures import ThreadPoolExecutor
from openAI.chatgpt.chatgpt import ChatGPT
import locale
import os
import openai

#regel van pareto


threads: List[AbstractThread] = []

def main():
  scraped_data = start_scraping()
  print(scraped_data)
  
  #prompt = ChatGPT().start_new_conversation(scraped_data)
  
  #print("TODO: dall-E generate link and send prompt: " + prompt)
  
def start_scraping():
  volatile_dict = VolatileDict()
  
  hln_thread = HLNThread(volatile_dict)
  deMorgen_thread = DeMorgenThread(volatile_dict)
  
  threads.append(hln_thread)
  threads.append(deMorgen_thread)
  with ThreadPoolExecutor() as pool:
    futures = [pool.submit(thread.start_scraping) for thread in threads]
  
  for future in futures:
    future.result()
    
  return volatile_dict.output_dict()  
  
  
  
if __name__ == "__main__":
  main()