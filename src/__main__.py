from threads.hlnThread import HLNThread
from threads.deMorgenThread import DeMorgenThread
from util.volatileDictionary import VolatileDict
from threads.abstractThread import AbstractThread
from typing import List
from concurrent.futures import ThreadPoolExecutor
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
  
  for i in volatile_dict.get_dict():
    print(volatile_dict.get_dict()[i])
  

if __name__ == "__main__":
  main()