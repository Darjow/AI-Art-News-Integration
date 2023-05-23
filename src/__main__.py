from openAI.chatgpt import ChatGPT
from openAI.dalle import DallE
from scraper.threads.StandaardScraper import StandaardScraper
from datetime import datetime


def main():
  date = datetime(2019, 4, 15)
  scraped_data = StandaardScraper(date).start_scraping()
  prompt = ChatGPT().start_new_conversation(scraped_data, date)
  image = DallE().generate_image(prompt)
  print(image)
  

  
if __name__ == "__main__":
  main()