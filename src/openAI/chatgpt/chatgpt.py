from openAI.util.openainrequesthandler import RequestHandler

class ChatGPT:
    def __init__(self):
        self.request_handler = RequestHandler()

#in nederlands
    def ask(self, data):
        prompt = f"""
        I would like to generate an artpiece with dall-e based on the highlights of today. Can you look at the different website uri's and 
        see which posts are similiar? If there are similiair posts, give me 1 sentance that combines these posts to generate an artpiece.  
        In the following json, u will find the following data : "website_uri" : [list of article titles]
        Just respond with the prompt for DallE.
    {data}\n"""
        response = self.request_handler.ask_chatgpt(prompt)
        return response.strip() 