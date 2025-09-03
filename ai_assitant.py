import os
import time
import os
import json
import google.generativeai as genai
import bot_tools

class AI_Agent():
    def __init__(self, api : str, prompt : str):
        self.api = api
        self.model = None
        self.chat_session = None
        self.prompt = prompt
        self.search_tools = None
    
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
        
    def _intitalize_agent(self):
        genai.configure(api_key=self.api)
        self.model = genai.GenerativeModel(self._get_available_model(), system_instruction=self.prompt)
        self.chat_session = self.model.start_chat(history=[])
    
    def _handle_message(self, chat_session: genai.ChatSession, question : str):
        tool_call_prompt = f"""
        You are a tool-calling agent. Your job is to decide if a user's question requires a search
        
        User's question: "{question}"
        
        If the question requires searching the knowledge base, respond with a JSON object.
        Example of your response: {{"tool_name": "search_by_keyword", "query": "KEYWORDS"}}.
        
        If the question can be answered without the search respond with "NO_TOOL_NEEDED".
        
        Your response must ONLY be the JSON string of "NO_TOOL_NEEDED".
        Do not add any other text.
        """
        
        llm_repsonse_text = self.chat_session.send_message(tool_call_prompt).text.strip()
        
        #Check is tools need to be used
        if llm_repsonse_text.upper() == "NO_TOOL_NEEDED":
            #No tool needed
            direct_response = self.chat_session.send_message(question).text
            return direct_response
        
        else:
            try:
                #Tools are needed
                start_index = llm_repsonse_text.find('{')
                end_index = llm_repsonse_text.rfind('}') + 1
                
                if start_index != -1 and end_index != -1:
                    json_string = llm_repsonse_text[start_index:end_index]
                    tool_call = json.loads(json_string)
                    
                    if tool_call.get("tool_name") == "search_by_keyword" and "query" in tool_call:
                        query = tool_call.get("query")
                        
                        search_results = self.search_tools.search_by_keyword(query)
                
                        search_result_prompt = f"""
                                You are a helpful assistant for the game Subnautica.
                                You have received the following information to answer the user's question.
                                        
                                User's original question: {question}
                                        
                                Search results:
                                {json.dumps(search_results, indent=2)}
                                        
                                Based on this information, provide a detailed and helpful answer.
                                
                                """
                        final_response = chat_session.send_message(search_result_prompt).text
                        return final_response
                    
                    else:
                        return "Error: Invalid tool call format from LLM."
                    
                else:
                    return "Error: LLM could not retrieve a valid JSON object."
                
            except json.JSONDecodeError:
                return "Error: Could not parse LLM's tool call response."
         
    def start_conversation(self):
        self._intitalize_agent()
        self.search_tools = bot_tools.Tools("subnautica_wiki.jsonl")
        continue_convo = True
        while continue_convo == True:
            question = input("What is your question? ")
            response = self._handle_message(self.chat_session ,question)
            print(response)
            
class Command_Handler():
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
            