from dotenv import load_dotenv
import os

load_dotenv()

def api_key():
  return os.environ.get("OPENAI_API_KEY")
