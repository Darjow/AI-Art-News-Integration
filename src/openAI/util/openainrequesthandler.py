from openAI.util import config
import requests
import openai

class RequestHandler:
    def __init__(self):
        openai.api_key =  config.api_key()

    def ask_chatgpt(self, prompt):
        response = openai.Completion.create(model="text-davinci-003", prompt=prompt, temperature=0, max_tokens=100)
        generated_text = response["choices"][0]["text"]

        return generated_text