from openAI.util import config
from dotenv import load_dotenv
import requests


class RequestHandler:
    def __init__(self):
        self.api_key = config.api_key()
        self.endpoint_url = "https://api.openai.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def ask_chatgpt(self, prompt, temperature=0.5):
        endpoint = self.endpoint_url + "/engines/davinci-codex/completions"
        print(prompt)
        payload = {
            "prompt": prompt,
            "temperature": temperature,        
        }
        response = requests.post(endpoint, json=payload, headers=self.headers)
        data = response.json()
        generated_text = data["choices"][0]["text"]


        return generated_text