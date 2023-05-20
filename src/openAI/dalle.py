from openAI.util.openairequesthandler import RequestHandler


class DallE:
  def __init__(self):
    self.request_handler = RequestHandler()
    
  def generate_image(self, prompt):
    return self.request_handler.generate_image(prompt)
