#Custom Imports
from db_tools.data_access import UserDataAccessor
from llm_assitant.llm_prompts import LLM_Prompts_Manager
from llm_assitant.lmm_tools import LLM_Tools

class LLM_Skeleton:
    def __init__(self):
        self.ADA = UserDataAccessor()
        self.current_messages = []
        self.summerized_messages = []
        self.prompts = LLM_Prompts_Manager()
        self.tools = LLM_Tools()
        
    def add_convo_summary(self, sum_convo : str):
        self.summerized_messages.append(sum_convo)
        
    def _update_user_up_time(self, userID : int):
        self.ADA.update_user_active_time(userID)
        
    def _save_conversation(self, convoID : int, user_content : str, agent_content : str):
        #Save to database
        self.ADA.add_new_message(convoID, user_content,"USER")
        self.ADA.add_new_message(convoID, agent_content, "AGENT"        )
        
        #Save to current memory for context later
        self.current_messages.append({"USER" : {user_content}, "AGENT" : {agent_content}})
        
    def _load_recent_chats_to_memory(self, userID):
        list_recent_convoID = []
        list_recent_convoID = self.ADA.get_recent_conversationsIDs(userID)
        return self.ADA.get_recent_messages(list_recent_convoID)
             
    def _tokenize_text(self, text: str) -> set[str]:
        #Elimates all unneeded words in history
        set_tokens = set()
        for word in text.split():
            word = word.lower()
            if len(word) > 2:
                set_tokens.add(word)
                
        return set_tokens
    
    def _preprocess_conversations(self, recent_memory : dict ):
        #Checks if message was tokenized else will tokenize it
        if recent_memory is None:
            return None
        
        for convo in recent_memory.values(): 
            messages = convo["message_details"]
            
            for msg in messages:
                if msg["role"] == "USER":
                    if not msg.get("tokens"):
                        msg["tokens"] = self._tokenize_text(msg["content"])
                
    def _jaccard_similarity(self, a: set, b: set) -> float:
        if not a or not b:
            return 0.0
        
        return len(a & b) / len(a | b)
    
    def _find_similar_question(self, question: str, threshold: float = 0.5) -> float:
        #Generate the question's tokens
        q_tokens = self._tokenize_text(question)
        
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
                        return prev_msg, score
                    
        return None, 0.0
         
        
    def is_context_needed(self, MSG_LIMIT : int = 10) -> str:
        if len(self.current_messages) <= MSG_LIMIT:
            return None
        else:
            context_prompt = self.prompts.need_context(self.summerized_messages)
            return context_prompt
    
    def get_determined_tool(self, question : str) -> str:
        return self.prompts.determine_tool_call(question)   
    
    def get_found_in_history(self, question : str, prev_question : str) -> str:
        return self.prompts.found_in_recent_chats(question, prev_question)
    
    def is_summary_needed(self, MSG_LIMIT : int = 10) -> str:
        if len(self.current_messages) >= MSG_LIMIT:
            sum_history_prompmt = self.prompts.summarize_current_message(self.current_messages)
            return sum_history_prompmt
        
        else:
            return None