from openAI.util import config
import requests
import openai

class RequestHandler:
  def __init__(self):
    openai.api_key =  config.api_key()

  def ask_chatgpt(self, conversation):  
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages = conversation)
    generated_text = response["choices"][0].message.content.strip()
    return generated_text