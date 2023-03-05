from openAI.util.openainrequesthandler import RequestHandler

class ChatGPT:
    def __init__(self):
        self.request_handler = RequestHandler()

    def get_response(self, data):
        prompt = f"""Human: 
        I would like to generate an artpiece with dall-e based on the highlights of today. 
        In the following json, u will find the following keys:
            - Base_url:  the website it has retrieved the article
            - Title: the title of the article. 
        Can you link the most similiar posts from the different base_urls to determine the highlights of the day? 
        What would be the prompt i would need to send to dall-e in order to generate an artpiece based of today?      
    {data}\nAI:"""
        response = self.request_handler.send_request(prompt, endpoint="/chat/completions")
        return response.strip()