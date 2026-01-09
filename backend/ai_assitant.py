from google import genai
from google.genai import types
from google.genai.errors import APIError, ClientError, ServerError
from data_access import UserDataAccessor
from user_template import User
from llm_prompts import LLM_Prompts_Manager

ADA = UserDataAccessor() #Agent Data Accessor

class Gemini_AI_Agent():
    def __init__(self, configs : dict, user : User):
        self.client = genai.Client()
        self.model = self._get_available_model(self.client)
        self.chat_session = None
        self.custom_configs = self._create_config_object(configs)
        self.prompts = LLM_Prompts_Manager()
        self.user_instance = user
        
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
    
    def _save_conversation(self, user_content : str, agent_content : str):
        ADA.add_new_message(self.user_instance.conversationID,
                            user_content,
                            "USER"        
        )
        
        ADA.add_new_message(self.user_instance.conversationID,
                            agent_content,
                            "AGENT"        
        )
        
    def _update_user_up_time(self):
        ADA.update_user_active_time(self.user_instance.userID)
        
    def _load_recent_chats(self, userID):
        list_recent_convoID = []
        list_recent_convoID = ADA.get_recent_conversationsIDs(userID)
        self.user_instance.recent_memory = ADA.get_recent_messages(list_recent_convoID)
        
    def initialize_agent_features(self, userID : int):
        #Load and Prep all features for the agent
        try:
            self._load_recent_chats(userID)
            
        except Exception as e:
            print(f"UNFORSEEN ERROR occurred during feature initialization: {e}")
        
    def _tokenize(text: str) -> set[str]:
        #Elimates all unneeded words in history
        set_tokens = set()
        for word in text.split():
            word = word.lower()
            if len(word) > 2:
                set_tokens.add(word)
                
        return set_tokens
    
    def _preprocess_conversations(self):
        #Checks if message was tokenized else will tokenize it
        for convo in self.user_instance.recent_memory.values():
            for msg in convo["message_details"]:
                if msg["role"] == "USER":
                    msg["tokens"] = self._tokenize(msg["content"])
                
    def _jaccard_similarity(a: set, b: set) -> float:
        if not a or not b:
            return 0.0
        
        return len(a & b) / len(a | b)
    
    def _find_similar_question(self, question: str, threshold: float = 0.5) -> float:
        #Generate the question's tokens
        q_tokens = self._tokenize(question)
        
        #Go through each message in a conversation
        for convo in self.user_instance.recent_memory.values():
            messages = convo.get("message_details", [])
            
            for i, msg in enumerate(messages):
                if msg["role"] != "USER":
                    continue
                
                tokens = msg["tokens"]
                if tokens is None:
                    continue
                
                score = self._jaccard_similarity(q_tokens, tokens)
                if score >= threshold:
                    #Get the reply the LLM gave
                    if i > 0:
                        prev_msg = messages[i - 1]
                        return prev_msg
    
    def _read_through_short_memory(self, question : str) -> str:
        if self.user_instance.recent_memory is None:
            return None
        
        try:
            self._preprocess_conversations()
            prev_message = self._find_similar_question(question)
            
            #Build Prompt for LLM
            return self.prompts.found_in_recent_chats(question, prev_message)
        
        except Exception as e:
            print(f"UNFORSEEN ERROR has occured during memory reading: {e}")
    
    def send_message(self, content : str) -> str:
        #Create new session on first talks
        if self.chat_session is None:
            self.chat_session = self.client.chats.create(
                model=self.model,
                config=self.custom_configs
                )
            
        #Seach recent conversations before LLm request
        updated_content = self._read_through_short_memory(content)
        if updated_content:
            content = updated_content
            
        #Send Message to the llm
        try:
            response_object = self.chat_session.send_message(content)
            
            #Make db changes accordingly
            try:
                self._save_conversation(content, response_object.text)
                self._update_user_up_time()
                
            except Exception as e:
                print(f"UNEXPECTED ERROR occured during save process : {e}")
                
            #Return agent response even if db goes sideways
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