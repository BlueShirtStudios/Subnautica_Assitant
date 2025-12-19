import os
import json
from google import genai
from google.genai import types
from google.genai.errors import APIError, ClientError, ServerError

class Gemini_AI_Agent():
    def __init__(self, configs : dict):
        self.client = genai.Client()
        self.model = self._get_available_model(self.client)
        self.chat_session = None
        self.custom_configs = self._create_config_object(configs)
        self.MAX_MEMORY_ENTRIES = 5
        self.session_chat_history = []

    def _get_available_model(self, client):
        available_model_name = None
        preferred_prefixes = ['gemini-2.5-flash', 'gemini-2.5-pro', 'gemini-flash-latest']
        
        found_suitable_models = []
        for m in client.models.list():
            model_name = m.name 
            if 'generateContent' in m.supported_actions: 
                for prefix in preferred_prefixes:
                    if model_name.startswith(f"models/{prefix}") or model_name == prefix:
                        found_suitable_models.append(m)
                        break
    
        for prefix in preferred_prefixes:
            for m in found_suitable_models:
                model_name = m.name 
                if model_name.startswith(f"models/{prefix}") or model_name == prefix:
                    available_model_name = model_name
                    break 
            if available_model_name:
                break
         
        if not available_model_name:
            print("ERROR: Could not find a suitable model for content generation.")
            exit() 
           
        return available_model_name
                   
    def _create_config_object(self, config_data: dict) -> types.GenerateContentConfig:
        #System Instruction for Agent
        system_instructions = config_data.get("system_prompt", None)
        
        generation_config = types.GenerateContentConfig(
            system_instruction=system_instructions
        )
        
        return generation_config
    
    def send_message(self, content : str) -> str:
        #Create new session on first talks
        if self.chat_session is None:
            self.chat_session = self.client.chats.create(
                model=self.model,
                config=self.custom_configs
                )

        #Send Message to the agent
        try:
            response_object = self.chat_session.send_message(content)
            return response_object.text
        
        #Handle errors accordingly
        except (ClientError, ServerError) as e:
            print("\n" + "="*50)
            print("CRITICAL API ERROR: Key/Quota Check Failed!")
            print(f"Error Details: {e}")
            print("This indicates an issue with your API key, region, or quota limits.")
            print("="*50 + "\n")
            exit()
        except Exception as e:
            print(f"\nUNEXPECTED ERROR while checking API status: {e}")
            exit()         
        
        
        