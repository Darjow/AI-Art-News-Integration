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
    
  def start_new_conversation(self, data):
    self.conversation = []
    
    self.ask("""
              Ik zou graag een kunstwerk willen genereren met dall-e gebaseerd op de hoogtepunten van vandaag. 
              Ik heb enkele artikels gevonden van vandaag, en deze gegroepeerd per url.
              Ik heb enkel de titel van het artikel opgeslaan. 
              Hoe eerder ze voorkomen hoe belangrijker ze zijn.
              """)
    
    self.ask(f"""
              Welke artikels zijn er het belangrijkst volgens jou, rekeninghoudend met vorige criteria. 
              Hieronder vind je de artikels in json formaat, gegroepeerd per url van belangrijk naar minder belangrijk. 
              
              {data}
              """)
    
    self.ask("Als je voor mij hier één kernzin kan uithalen; een samenvatting. Welke zou het dan zijn?")
    
    self.ask("Maak voor mij een kernboodschap op basis van voorgaand JSON. Houd de boodschap beperkt zodat het zeker duidelijk is in het kunstwerk.")
    
    self.ask("""
              Ik zou dit nu graag laten genereren door dall-e om een kunstwerk te krijgen. 
              Wat zou een goede prompt kunnen zijn die een kernboodschap weergeeft van de artikels?
              Vergeet geen schilder en stijl erbij te zeggen.
              """)
    
    data = self.ask("Reageer enkel met een prompt en zet deze tussen quotes zet er ook bij door welke kunstenaar deze is geschilderd.")
  
    
    self.ask("Op basis van welke kernartikels heb je dit gehaald?")
    
    return data        
    
    
  def append_to_conversation(self, role, message):
    print(f"{role}: {message}\n")
    self.conversation.append({"role": role, "content": message})
    
