from openAI.util.openairequesthandler import RequestHandler


class ChatGPT:
  def __init__(self):
    self.request_handler = RequestHandler()
    self.conversation = []

  def ask(self, prompt):
    self.append_to_conversation("user", prompt)
    response = self.request_handler.ask_chatgpt(self.conversation)
    self.append_to_conversation("assistant", response)
    
    return response
    
  def start_new_conversation(self, data, date):
    self.conversation = []
    
    self.ask(f"""
              Ik zou graag een kunstwerk willen genereren met dall-e gebaseerd op de hoogtepunten van {date.day} {date.month} {date.year}. 
              Ik heb enkel de titel van het artikel opgeslaan. 
              """)
    
    self.ask(f"""
              Welke artikels zijn er het belangrijkst volgens jou, rekeninghoudend met vorige criteria. 
              Hieronder vind je de artikels.
              
              {data}
              """)
    
    self.ask("Als je voor mij hier één kernzin kan uithalen; een samenvatting. Welke zou het dan zijn?")
    
    self.ask("Maak voor mij een kernboodschap op basis van voorgaande artikels. Houd de boodschap beperkt tot één artikel.")
    
    self.ask("""
              Ik zou dit nu graag laten genereren door dall-e om een kunstwerk te krijgen. 
              Wat zou een goede prompt kunnen zijn die een kernboodschap weergeeft van de belangrijkste artikel, de boodschap moet goed overkomen.
              Vergeet geen stijl erbij te zeggen.
              """)
    
    data = self.ask("Reageer enkel met een prompt die deze kernboodschap weergeeft en zet deze tussen quotes zet er ook bij door welke kunstenaar deze is geschilderd of in welke stijl. Gebruik maximum 75 karakters.")
  
    
    self.ask("Op basis van welke kernartikels heb je dit gehaald?")
    
    return data        
    
    
  def append_to_conversation(self, role, message):
    print(f"{role}: {message}\n")
    self.conversation.append({"role": role, "content": message})
    
