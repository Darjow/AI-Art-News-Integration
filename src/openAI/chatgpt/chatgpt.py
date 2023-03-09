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
        
        self.ask(f"""
            Ik zou graag een kunstwerk willen genereren met dall-e, gebaseerd op de hoogtepunten van vandaag. 
            Kun je kijken naar de verschillende artikels en zien welke artikels overeenkomen met artikels van een andere website_uri?
            Als er overeenkomstige berichten zijn, dan wil ik dat ze prioritair zijn ten opzichte van andere artikels.
            Geef me dan één zin die deze berichten combineert samen met een kunstenaal om een kunstwerk te genereren. 
            Deze zin moet een duidelijke boodschap weergeven van de hoogtepunten van de dag en moet als een prompt voor Dall-e voorzien worden.
            In de volgende JSON vind je de volgende gegevens: "website_uri": [lijst van artikel titels]. \n
            
            {data}\n
            
            """)
        
        
        #backup als parsing faalt: jij:     'De prompt die ik zou aanbieden is: "Een wereldkaart met verschillende kleuren om de politieke, economische, militaire en technologische conflicten te symboliseren, geschilderd door Banksy.'
        data = self.ask("Reageer enkel met een prompt, en in een specifieke stijl en/of door een specifieke kunstenaar.")
        
        try:
          data = data.split('"')[1]
        except:
          pass    
        
        self.ask("Op basis van welke kernartikels heb je dit gehaald?")
        
        return data        
        
        
    def append_to_history(self, data):
        print(data + '\n')
        self.conversation.append(data)
        
