from scraper.threads.hlnThread import HLNThread
from scraper.threads.deMorgenThread import DeMorgenThread
from scraper.util.volatileDictionary import VolatileDict
from scraper.threads.abstractThread import AbstractThread
from typing import List
from concurrent.futures import ThreadPoolExecutor
from openAI.chatgpt.chatgpt import ChatGPT
import locale

threads: List[AbstractThread] = []

def main():
  locale.setlocale(locale.LC_TIME, 'nl_NL.utf8')

  volatile_dict = VolatileDict()
  
  hln_thread = HLNThread(volatile_dict)
  deMorgen_thread = DeMorgenThread(volatile_dict)
  
  threads.append(hln_thread)
  threads.append(deMorgen_thread)
  with ThreadPoolExecutor() as pool:
    futures = [pool.submit(thread.start_scraping) for thread in threads]
  
  for future in futures:
    future.result()
    
  parsed_data = volatile_dict.output_json()
  print(parsed_data)
  
  chad = ChatGPT()
  chad.get_response(parsed_data)
  
  

if __name__ == "__main__":
  main()