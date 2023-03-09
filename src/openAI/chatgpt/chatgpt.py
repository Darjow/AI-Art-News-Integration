from openAI.util.openainrequesthandler import RequestHandler


INIT_CONV = "Dit is ons gesprek houd hier rekening mee, en reageer op het laatste bericht. "
class ChatGPT:
    def __init__(self):
        self.request_handler = RequestHandler()
        self.conversation = [INIT_CONV]

    def ask(self, prompt):
        self.add_chat(prompt, False)
        response = self.request_handler.ask_chatgpt(self.conversation)
        self.add_chat(response, True)
        
        return response
    
    def start_new_conversation(self, data):
        self.conversation = [INIT_CONV]
        
        self.ask(f"""
            Ik zou graag een kunstwerk willen genereren met dall-e, gebaseerd op de hoogtepunten van vandaag. 
            Kun je kijken naar de verschillende website uri's en zien welke berichten van de verschillende
            website_uri's overeenkomen met elkaar? 
            Als er overeenkomstige berichten zijn, geef me dan één zin die deze berichten combineert om een kunstwerk
            te genereren. Dit kan een specifiek gevoel/thema of boodschap overbrengen.
            In de volgende JSON vind je de volgende gegevens: "website_uri": [lijst van artikel titels]. \n
            
            {data}\n""")
        
        self.ask("wat vroeg ik net aan je ?")
    
    def append_to_history(self, data):
        print(data)
        self.conversation.append(data)
        
        
    
    def add_chat(self, chat, chatgpt):
        if chatgpt:
            self.append_to_history(f"jij: {chat}\n")
        else:
            self.append_to_history(f"ik: {chat}\n")
