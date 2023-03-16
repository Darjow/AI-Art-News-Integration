from openAI.util.openainrequesthandler import RequestHandler


class ChatGPT:
    def __init__(self):
        self.request_handler = RequestHandler()
        self.conversation = []

    def ask(self, prompt):
        self.append_to_history(prompt)
        response = self.request_handler.ask_chatgpt(self.conversation)
        self.append_to_history(response)
        
        return response
    
    def start_new_conversation(self, data):
        self.conversation = []
        
        self.ask("""
                 Ik zou graag een kunstwerk willen genereren met dall-e gebaseerd op de hoogtepunten van vandaag. Ik heb enkele artikels gevonden van vandaag.
                 Kun jij voor mij bepalen welke artikels met een verschillende website_url gelijkenissen hebben?                 
                 """)
        
        self.ask(f"""
                 Welke artikels zijn er het belangrijkst als je afgaat op vaakst voorkomende artikel met verschillend website urls?
                 Hieronder vind je de artikels in json formaat. Ik wil dat je een boodschap of thema hieruit haalt
                 [website_url : [artikels], ... ]
                 
                 {data}
                 """)
        
        self.ask("Als je voor mij hier één kernzin kan uithalen; een samenvatting. Welke zou het dan zijn?")
        
        self.ask("Maak voor mij een kernboodschap op basis van voorgaand JSON.")
        
        self.ask("""
                 Ik zou dit nu graag laten genereren door dall-e om een kunstwerk te krijgen. 
                 Wat zou een goede prompt kunnen zijn die een kernboodschap weergeeft van de artikels? Vergeet geen schilder of stijl erbij te zeggen.
                 """)
        
        data = self.ask("Reageer enkel met een prompt en zet deze tussen quotes zet er ook bij door welke kunstenaar deze is geschilderd.")
      
        
        self.ask("Op basis van welke kernartikels heb je dit gehaald?")
        
        return data        
        
        
    def append_to_history(self, data):
        print(data + '\n')
        self.conversation.append(data)
        
