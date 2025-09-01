import os
import time
import json
import google.generativeai as genai

class AI_Assitant():
    def __init__(self, api : str, prompt : str):
        self.api = api
        self.model = None
        self.prompt = prompt
        self.chat_history_list = []
        self.continue_convo = False
        
    def get_api(self):
        return self.api
    
    def set_api(self, api : str):
        self.api = api
        
    def get_prompt(self):
        return self.prompt
    
    def set_prompt(self, prompt : str):
        self.prompt = prompt
        
    def get_chat_history(self):
        return self.chat_history_list
    
    def add_to_chat_history(self, role : str, content : str):
        self.chat_history_list.append(role, content)
        
    def get_continue_convo(self):
        return self.continue_convo
    
    def set_continue_convo(self, repsonse : bool):
        self.continue_convo = repsonse
        
    def get_model(self):
        return self.model
    
    def set_model(self, model : str):
        self.model = model
        
    def _get_available_model(self):
        available_model_name = None
        print("------------Model loading begun-------------")
        print("Attempting to list available models and select a suitable one...")

        preferred_prefixes = ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']
    
        #Store models that meet criteria to pick the best later
        found_suitable_models = []

        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                for prefix in preferred_prefixes:
                    if m.name.startswith(prefix):
                        found_suitable_models.append(m)
                        break

        for prefix in preferred_prefixes:
            for m in found_suitable_models:
                if m.name.startswith(prefix):
                    available_model_name = m.name
                    print(f"Prioritizing and using model: {available_model_name}")
                    break 
            if available_model_name:
                break

        if available_model_name:
            print(f"Final selected model: {available_model_name}")
            #Everthing is fine if it came to this point
            print("------------Model loading complete-------------")
        
            return available_model_name
        else:
            print("Error: No suitable model found that supports 'generateContent' in your environment.")
            print("Please ensure you have access to Gemini 1.5 models (e.g., gemini-1.5-flash-00X) or gemini-pro.")
            print("Here are all models available to your API key that support generateContent:")
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    print(f"- {m.name}")
            exit()
        
    def _intitalize_bot(self):
        genai.configure(api_key=self.get_api())
        
        self.set_model(genai.GenerativeModel(self._get_available_model(), system_instruction=self.get_prompt()))
        chat = self.get_model().start_chat(history=self.get_chat_history())
        return chat
    
    def _get_response(self, chat : str, question : str):
        repsonse = chat.send_message(question).text
        return repsonse
        
    def start_conversation(self):
        chat = self._intitalize_bot()
        self.set_continue_convo(True)
        print("Hello I am ALT.")
        while self.get_continue_convo:
            user_question = input("What is your question?")
            print(self._get_response(chat, user_question))
            
class Commands(AI_Assitant):
    def __init__(self):
        self.commands_dict ={
            "exit": {
                "method": self.exit,
                "description": "Exits the program"
            },
            "help": {
                "method": self.help,
                "description": "Exits the program"
            },
            "new": {
                "method": self.new,
                "description": "Starts new Chat"
            }   
        }
    def handle_command(self, command):
        command = command.strip().lower()
        if command in self.commands_dict:
            self.commands_dict["method"[command]]()
            return True
        else:
            return False
        
    def handle_exit(self):
        print("Closing ALT. Safe travels survivior...")
        
    def handle_help(self):
        print("Loading command dictionary...")
        for cmd, info in self.commands_dict:
            print(f"- {cmd} : {info["description"]}")
            