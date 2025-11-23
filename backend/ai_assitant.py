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
        self.MAX_MEMORY_ENTRIES = 5
        self.chat_history = []
        self.chat_history_path = chat_history_file_path
        self.assit_commands = Assit_Commands(self)
        self.tools = None
    
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
        #Configure Agent
        genai.configure(api_key=self.api)
        self.model = genai.GenerativeModel(self._get_available_model(), system_instruction=self.prompt)
        
        #Check if knowledge base can be reached + Get Tools File
        data_path = os.path.join(os.path.dirname(__file__), "data", "subnautica_wiki.jsonl")
        if os.path.exists(data_path):
            self.tools = bot_tools.Tools(data_path)
            
        else:
            return "Tools not found, Critical Error"
        
        #Load past chats to memory
        if os.path.exists(self.chat_history_path):
            if os.stat(self.chat_history_path).st_size > 0:
                self.assit_commands.handle_load_conversation(self.chat_history_path)
                
        else:
            #Create history if file does not exists
            self.chat_history_path = self.assit_commands.create_chat_history_file()
        
        #Establish Session
        self.chat_session = self.model.start_chat(history=[])
        
    def restart_session(self):
        self.chat_session = self.model.start_chat(history=[])
        self.chat_history = []
        self.assit_commands.deliver_Output("Chat has been restarted.")
        
    def save_short_term(self, combined_entry : dict):
        if (len(self.chat_history) >= self.MAX_MEMORY_ENTRIES):
            self.assit_commands.deliver_Output("Memory is full. Removing oldest conversation from short term memory.")
            self.chat_history.pop(0)
            self.chat_history.append(combined_entry)
        
        else:
            self.chat_history.append(combined_entry)
                     
    def _handle_message(self, question : str):#format die output mooier, soos spasie en watnot
        user_message_object = {"role": "user", "parts": [{"text": question}]}
        
        #First look in short-term memory
        if self.chat_history:
            is_relevant = self.tools.scan_history(self.chat_history, question)
            if is_relevant:
                return is_relevant
        
        #Determine if tool is to be used
        llm_tool_request_result = self.is_tool_needed(question)
        if llm_tool_request_result != "NO_TOOL_NEEDED":
            tool_call = self.call_desired_tool(llm_tool_request_result)
            model_response_object = self.use_tool_for_response(tool_call, question)
            
        else:
            model_response_object = self.chat_session.send_message(question)
            
        final_response = model_response_object.text     

        #Save to short-term memory
        combined_entry = self.tools.formatEntry(question, final_response)
        self.save_short_term(combined_entry)
        
        #Save a summarized version of the chats
        self.summarize_convos_save(combined_entry)
            
        #Return response 
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
        
        if llm_repsonse_text.upper() != "NO_TOOL_NEEDED":
            return llm_repsonse_text
        else:
            return "NO_TOOL_NEEDED"
                     
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
        #Extract details according to type of tool     
        if tool_call.get("tool_name") == "search_by_keyword" and "query" in tool_call:
            query = tool_call.get("query")
                        
            search_results = self.tools.search_by_keyword(query)
                
            search_result_prompt = f"""
            You are a helpful assistant for the game Subnautica.
            You have received the following information to answer the user's question.
                                        
            User's original question: {question}
                                        
            Search results:
            {json.dumps(search_results, indent=2)}
                                        
            Based on this information, provide a detailed and helpful answer.
                                
            """
            final_response = self.chat_session.send_message(search_result_prompt)
            return final_response
                        
        else:
            return "Error: LLM could not retrieve a valid JSON object."
        
        
    def summarize_convos_save(self, entry): #fix die later, logic and implemetation errors
        summarize_entry_prompt = f"""You are an agent that specilies in summarization. You need to summarize the follow content of the list 
                                as one usefull summary so that other agents can use to assit them in querie. 
                                
                                Unsummirised Entry : {entry}
                                
                                Ensure that the summary is done perfect, keep any keywords that is present to ensure
                                an accurate summary of the entry.
                                """
                                
        summairized_entry = self.chat_session.send_message(summarize_entry_prompt).text
        self.assit_commands.handle_save_conversation(self.chat_history_path, summairized_entry)                     

class Assit_Commands():
    def __init__(self, agent_instance):
        self.agent = agent_instance
        self.commands = {
                "exit" : self.handle_exit,
                "help": self.handle_help,
                "clear": self.handle_clear_terminal,
                "ouput": self.deliver_Output,
                "create": self.create_chat_history_file,
                "load": self.handle_load_conversation,
                "save": self.handle_save_conversation,
                "new": self.handle_new_conversation,
                "info": self.handle_info,
                "view_chats": self.handle_view_history,
                "clean_history": self.handle_clean_history
        }
        self.developer_reserved_command = ["output", 
                                           "create", 
                                           "load", 
                                           "save"]
        
    def run_command(self, line : str):
        parts = line[1:].strip().split()
        cmd = parts[0]
        if len(parts) > 1:
            arg = parts[1:][0]
            
        else:
            arg = None
            
        if cmd in self.developer_reserved_command:
            self.deliver_Output(f"Entered Commad: {cmd}, is a internal command only for development use.")
        
        if cmd in self.commands:
            self.commands[cmd](arg)
        
        else:
            self.deliver_Output(f"Unknown Command Present: cmd - {cmd}")
        
    def handle_exit(self, args=None):
        self.deliver_Output("Closing ALT. Safe travels survivior...")
        exit()
        
    def handle_help(self, args=None):
        #Used in development for easy access + adds transparency 
        self.deliver_Output("Loading command dictionary...")
        for cmd, info in self.commands_dict.items():
            self.deliver_Output(f"- {cmd} : {info["description"]}")
            
    def handle_new_conversation(self, args=None):
        self.agent.restart_session()
        self.agent.chat_history.append("New Session Started.")
        self.handle_clear_terminal()
            
    def handle_clear_terminal(self, args=None):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
            
    def create_chat_history_file(self, args = None):
        self.deliver_Output("File not found. Creating new history...")
        relative_user_path = os.path.join(os.getcwd(), "user_data");
        os.makedirs(relative_user_path, exist_ok=True)
        chat_dir_path = os.path.join(relative_user_path, "chat_history.jsonl")
        with open(chat_dir_path, "w") as f:
            pass
        
        return chat_dir_path
            
    def handle_load_conversation(self, file_path : str, limit = 10):
        #Check if the history file can be located
        if not file_path:
            self.deliver_Output("Please provide path to file or filename")
            return        

        #Load history to chat history
        loaded_history = []
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                all_lines = file.readlines()           
                reversed_lines = all_lines[::-1]
                
                lines_to_process = reversed_lines[::limit]
                for lines in lines_to_process:
                    if lines.strip():
                        loaded_history.append(json.loads(lines))
                    
        except json.JSONDecodeError:
            self.deliver_Output("Error: Failed to decode JSON.")
            
        except FileNotFoundError:
            loaded_history = []
            
        except Exception as e:
            self.deliver_Output(f"An error has occured during loading: {e}")
            
        self.agent.chat_history = loaded_history
                    
    def handle_save_conversation(self, file_path : str, line_to_save : str ):
        if not file_path:
            self.deliver_Output("Please provide path to file or filename")
            return
        
        if not os.path.exists(file_path):
            self.deliver_Output("Critical Error: History file not found.")
            return
        
        saveable_line = {"summary": line_to_save}
            
        try:
            json_line = json.dumps(saveable_line)
            with open(file_path, "a", encoding="utf-8") as file:
                file.flush()
                file.write(json_line + "\n")
                    
        except Exception as e:
                self.deliver_Output(f"An error has occured: {e}")
            
    def handle_info(self, args=None):
        self.deliver_Output("Name: ALT")
        self.deliver_Output("LLM Model: Gemini")
        self.deliver_Output("Description: Assistant for User")
        
    def deliver_Output(self, output_phrase : str): #Potencial modes to come..
        print(output_phrase)
        
    def handle_view_history(self, filepath : str):
        self.deliver_Output("Presenting History From Most Recent Chats...")
        
    def handle_clean_history(self, filepath):
        open(filepath, "w").close()