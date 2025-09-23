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
        self.chat_history = []
        self.search_tools = None
        self.commands = Command_Handler(self)
    
    def _get_available_model(self):
        available_model_name = None
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
                    break 
            if available_model_name:
                break

        if available_model_name:
            return available_model_name
        
        else:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    print(f"- {m.name}")
            exit()
        
    def intitalize_agent(self):
        genai.configure(api_key=self.api)
        self.model = genai.GenerativeModel(self._get_available_model(), system_instruction=self.prompt)
        
        data_path = os.path.join(os.path.dirname(__file__), "data", "subnautica_wiki.jsonl")
        if os.path.exists(data_path):
            self.search_tools = bot_tools.Tools(data_path)
            
        else:
            print("Error 001")
        
        if os.path.exists("chat_history.json"):
            if os.stat("chat_history.json").st_size > 0:
                self.commands.handle_load("chat_history.json")
            
        self.chat_session = self.model.start_chat(history=[])
        
    def restart_session(self):
        self.chat_session = self.model.start_chat(history=[])
        self.chat_history = []
        print("Chat has been restarted.")
        
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
            
class Command_Handler():
    def __init__(self, agent_instance):
        self.agent = agent_instance
        self.exit = self.handle_exit
        self.help = self.handle_help
        self.new = self.handle_new
        self.load = self.handle_load
        self.save = self.handle_save
        self.clear = self.handle_clear
        self.history = self.handle_history
        self.info = self.handle_info
        self.commands_dict ={
            "exit": {
                "method": self.exit,
                "description": "Exits the program"
            },
            "help": {
                "method": self.help,
                "description": "Display all commands"
            },
            "new": {
                "method": self.new,
                "description": "Starts new Chat"
            },
            "load":{
                "method": self.load,
                "description": "Load previous Chat from File [args : File Path ; str]"
            },
            "save":{
                "method": self.save,
                "description": "Save Chat to File [args : File Path : str]"
            },
            "clear":{
                "method": self.clear,
                "description": "Clean Console Output"
            },
            "history":{
                "method": self.history,
                "description": "Brings history of Chat"
            },
            "info":{
                "method": self.info,
                "description": "Gives Info on Agent"
            }
        }
        
    def handle_command(self, command_input):
        parts = command_input.strip().lower().split()
        command = parts[0]
        args = parts[1:]
        
        if command in self.commands_dict:
            method_call = self.commands_dict[command]["method"]
            method_call(args)
            return True
        else:
            return False
        
    def handle_exit(self, args=None):
        print("Closing ALT. Safe travels survivior...")
        exit()
        
    def handle_help(self, args=None):
        print("Loading command dictionary...")
        for cmd, info in self.commands_dict.items():
            print(f"- {cmd} : {info["description"]}")
            
    def handle_new(self, args=None):
        self.agent.restart_session()
        self.agent.chat_history.append("New Session Started.")
        self.handle_clear()
            
    def handle_clear(self, args=None):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
            
    def handle_load(self, args):
        if not args:
            print("Please provide path to file or filename")
            return
        
        if not isinstance(args, list):
            file_path = args
        
        if not os.path.exists(file_path):
            print("File not found.")
            return
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                loaded_history = json.load(file)
                if isinstance(loaded_history, list):
                    self.agent.chat_history = loaded_history
                else:
                    print("There was an issue: Loaded History is not list")
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON.")
            
        except Exception as e:
            print(f"An error has occured during loading: {e}")
                    
    def handle_save(self, args):
        if not args:
            print("Please provide path to file or filename")
            return
        
        if not isinstance(args, list):
            file_path = args
        
        if not os.path.exists(file_path):
            print("File not found.")
            return
        else:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    json.dumps(self.agent.chat_history, file, indent=4)
                    print("Chat history saved.")
                    
            except Exception as e:
                print(f"An error has occured: {e}")
                
    def handle_history(self, args=None):
        for lines in self.agent.chat_history:
            print(lines)
            
    def handle_info(self, args=None):
        print("Name: ALT")
        print("LLM Model: Gemini")
        print("Description: Assistant for User")