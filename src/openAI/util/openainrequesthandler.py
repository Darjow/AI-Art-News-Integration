from openAI.util import config
from dotenv import load_dotenv


class RequestHandler:
    def __init__(self):
        self.api_key = config.api_key()
        self.endpoint_url = "https://api.openai.com/v1"

    def send_request(self, prompt, endpoint, model="text-davinci-002", temperature=0.5):
        
        payload = {
            "prompt": prompt,
            "temperature": temperature,
            "model": model,
            "stop": ["\n", "Human:", "AI:"]
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(self.endpoint_url+endpoint, json=payload, headers=headers)
        data = response.json()
        generated_text = data["choices"][0]["text"]

        return generated_text