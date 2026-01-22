from google import genai
from google.genai import types
from google.genai.errors import APIError, ClientError, ServerError

#Custom Imports
from user_template import User
from llm_assitant.llm_config import LLM_CONFIGS
from llm_assitant.llm_skeleton import LLM_Skeleton

class Gemini_AI_Agent():
    def __init__(self, user : User):
        self.user_instance = user
        self.skeleton = LLM_Skeleton()
        self.client = genai.Client()
        self.chat_session = None
        self.model = self._get_available_model(self.client)
        self.custom_configs = self._create_config_object(LLM_CONFIGS)
        
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
    
    def initialize_agent(self):
        try:
            self._initialize_session()
            self.user_instance.recent_memory = self.skeleton._load_recent_chats_to_memory(self.user_instance.userID)
            
        except Exception as e:
            print(f"UNFORSEEN ERROR occurred during feature initialization: {e}")
      
    
    def _initialize_session(self):
        self.chat_session = self.client.chats.create(
                model=self.model,
                config=self.custom_configs
                )
            
    def send_text_filled_message(self, main_content : str) -> str:
        #Create new session on first talk
        if self.chat_session is None:
            self._initialize_session()
            
        try:
            #Send Message to the llm
            response_object = self.chat_session.send_message(main_content)
                
            #Return llm response allways
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
            
    def _use_rag_system(self, question : str) -> str:
        #Use Custom RAG tools to get accurate information on the question
        try:
            determined_tool = self.skeleton.get_determined_tool(question)
            tool_call_response = self.send_text_filled_message(determined_tool)
            self.skeleton.tools.update_tools_status(question, tool_call_response)
            self.skeleton.tools.use_tool()
            retrieved_info = self.skeleton.tools.fetch_results()
            if retrieved_info is None:
                return None
            
            return self.skeleton.prompts.info_on_question_found(retrieved_info)
        
        except Exception as e:
            print(f"An error occured during RAG Retrieval: {e}")
        
    def _scan_recent_history(self, question : str) -> str:
        try:
            #Use history features to  check question like existed
            if self.user_instance.recent_memory is None or len(self.user_instance.recent_memory) < 1:
                return None, 0.0
            
            self.skeleton._preprocess_conversations(self.user_instance.recent_memory)
            result = self._find_similar_question(question)
            
            if result is None:
                return None, 0.0
            
            prev_message, score = result
            
            improved_prompt = self.skeleton.get_found_in_history(question, prev_message)
            return improved_prompt, score
            
        except Exception as e:
            print(f"An error occured during Hisotry Scan: {e}")
        
    def _summarize_messages(self):
        sum_history_prompt = self.skeleton.prompts.summarize_current_message()
        response_object = self.send_text_filled_message(sum_history_prompt)   
        self.skeleton.add_convo_summary(response_object.text)
        
    def _fetch_context_if_needed(self):
        prompt = self.skeleton.is_context_needed()
        if prompt is None:
            return None
        
        self.send_text_filled_message(prompt)
        
    def start_chatting(self, sent_content : str) -> str:
        #Run Through the whole prompt refinement process (my mini orcastrastion)
        improved_prompt, accuraccy_score = self._scan_recent_history(sent_content)
        if accuraccy_score < 0.4:
            improved_prompt = self._use_rag_system(sent_content)
            if improved_prompt is None:
                text_response = self.send_text_filled_message(sent_content)
            
        else:
            text_response = self.send_text_filled_message(improved_prompt)
                
        return text_response