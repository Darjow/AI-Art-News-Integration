from threads.hlnThread import HLNThread
from util.volatileDictionary import VolatileDict
from threads.abstractThread import AbstractThread
from typing import List
from concurrent.futures import ThreadPoolExecutor

threads: List[AbstractThread] = []

def main():
  volatile_dict = VolatileDict()
  
  hln_thread = HLNThread(volatile_dict)
  threads.append(hln_thread)
  
  with ThreadPoolExecutor() as pool:
    futures = [pool.submit(thread.start_scraping) for thread in threads]
  
  for future in futures:
    future.result()
  

if __name__ == "__main__":
  main()