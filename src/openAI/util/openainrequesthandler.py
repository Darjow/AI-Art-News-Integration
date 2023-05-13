from openAI.util import config
import requests
import openai

class RequestHandler:
    def __init__(self):
        openai.api_key =  config.api_key()

    def ask_chatgpt(self, conversation):
        _prompt = f"reageer op volgende gesprek: {conversation}"
        response = openai.Completion.create(
          model="gpt-3.5-turbo",
          messages = [
            {"role": "user", "content": _prompt}
          ])
          
        generated_text = response["choices"][0]["text"].strip()
        return generated_text