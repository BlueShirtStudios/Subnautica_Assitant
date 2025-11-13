import os
import json
import google.generativeai as genai
import bot_tools

class AI_Agent():
    def __init__(self, api : str, prompt : str, chat_history_file_path : str):
        self.api = api
        self.model = None
        self.chat_session = None
        self.prompt = prompt
        self.chat_history = []
        self.chat_history_path = chat_history_file_path
        self.assit_commands = Assit_Commands(self)
    
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
            return "Tools not found, Critical Error"
        
        if os.path.exists(self.chat_history_path):
            if os.stat("chat_history.json").st_size > 0:
                self.assit_commands.handle_load_conversation(self.chat_history_path)
            
        self.chat_session = self.model.start_chat(history=[])
        
    def restart_session(self):
        self.chat_session = self.model.start_chat(history=[])
        self.chat_history = []
        self.assit_commands.deliver_Output("Chat has been restarted.")
        
    def _handle_message(self, chat_session: genai.ChatSession, question : str):
        if self.is_tool_needed(question):
            tool_call = self.call_desired_tool
            final_response = self.use_tool_for_response(tool_call, question)
            
        else:
            final_response = self.chat_session.send_message(question) 
            
        self.chat_history = {"question" : question, "agent" : final_response}
            
            
        #return result to app
        return final_response
            
    def is_tool_needed(self, question : str):
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
        
        if llm_repsonse_text.upper() == "NO_TOOL_NEEDED":
            return False
        
        else:
            return True
                     
    def call_desired_tool(self, llm_response_text):
        #Clean llm respnse to see what tool is called
        try:
            start_index = llm_response_text.find('{')
            end_index = llm_response_text.rfind('}') + 1
                
            if start_index != -1 and end_index != -1:
                json_string = llm_response_text[start_index:end_index]
                tool_call = json.loads(json_string)
                return tool_call
                
            else:
                return "Error: Invalid tool call format from LLM."
                
        except json.JSONDecodeError:
                return "Error: Could not parse LLM's tool call response."
             
    def use_tool_for_response(self, tool_call : str, question : str):       
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
            final_response = self.chat_session.send_message(search_result_prompt).text
            return final_response
                        
        else:
            return "Error: LLM could not retrieve a valid JSON object."
                                
class Assit_Commands():
    def __init__(self, agent_instance):
        self.agent = agent_instance
        self.exit = self.handle_exit
        self.help = self.handle_help
        self.new_converstaion = self.handle_new_converstaion
        self.load_conversation = self.handle_load_converstaion
        self.save_conversation = self.handle_save_converstaion
        self.clear_terminal = self.handle_clear_terminal
        self.conversation_history = self.converstaion_handle_history
        self.agent_info = self.handle_info
        self.deliver_Output = self.deliver_Output
        
    def handle_exit(self, args=None):
        self.deliver_Output("Closing ALT. Safe travels survivior...")
        exit()
        
    def handle_help(self, args=None):
        self.deliver_Output("Loading command dictionary...")
        for cmd, info in self.commands_dict.items():
            self.deliver_Output(f"- {cmd} : {info["description"]}")
            
    def handle_new_conversation(self, args=None):
        self.agent.restart_session()
        self.agent.chat_history.append("New Session Started.")
        self.handle_clear()
            
    def handle_clear_terminal(self, args=None):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
            
    def handle_load_conversation(self, file_path : str):
        #Check if the history file can be located
        if not file_path:
            self.deliver_Output("Please provide path to file or filename")
            return        

        if not os.path.exists(file_path):
            #Create history file if not exists
            self.deliver_Output("File not found. Creating new history...")
            chat_dir_path = "data"
            os.makedirs(chat_dir_path, exist_ok=True)
            chat_dir_path = os.path.join(chat_dir_path, "chat_history.json")
            newChatFile = open(chat_dir_path, "w")
            file_path = newChatFile
        
        #Load history to chat history
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                loaded_history = json.load(file)
                #Add cap op convos wat load na bot
                
                if isinstance(loaded_history, list):
                    self.agent.chat_history = loaded_history
                    
                else:
                    self.deliver_Output("There was an issue: Loaded History is not list")
                    
        except json.JSONDecodeError:
            self.deliver_Output("Error: Failed to decode JSON.")
            
        except Exception as e:
            self.deliver_Output(f"An error has occured during loading: {e}")
                    
    def handle_save_conversation(self, file_path : str):
        if not file_path:
            self.deliver_Output("Please provide path to file or filename")
            return
        
        if not os.path.exists(file_path):
            self.deliver_Output("Critical Error: History file not found.")
            return
            
        try:
            with open(file_path, "a", encoding="utf-8") as file:
                    json.dumps(self.agent.chat_history, file, indent=4)
                    self.deliver_Output("Chat history saved.")
                    
        except Exception as e:
                self.deliver_Output(f"An error has occured: {e}")
                
    def handle_history_conversation(self, args=None):
        for lines in self.agent.chat_history:
            self.deliver_Output(lines)
            
    def handle_info(self, args=None):
        self.deliver_Output("Name: ALT")
        self.deliver_Output("LLM Model: Gemini")
        self.deliver_Output("Description: Assistant for User")
        
    def deliver_Output(self, output_phrase : str): #Potencial modes to come..
        print(output_phrase)