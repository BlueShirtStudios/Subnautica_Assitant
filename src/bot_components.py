import json
import os

""" MODULE DESCRIPTION
Contains both the Knowledgebase class and PromptManager class. The Knowledgebase uses the json file (knowledge_base.json)
to get the needed information to help to construct a proper prompt using the PromptManager class
"""

class KnowledgeBase:
    """
    filename (str) : The file containing the data
    data (str) : Information we extract from the file
    """
    def __init__(self, filename="knowledge_base.json", data = None):
        self.filename = os.path.join("src", filename)
        self.data = data
        self._load_data()
        
    def _set_data(self, data):
        self.data = data
        
    def _load_data(self):
        #Attempt to open File
        try:
            with open(self.filename, "r") as f:
                self._set_data(json.load(f))
        except FileNotFoundError:
            print(f"Error: '{self.filename}' not found. Please run build_knowledge_base.py.")
            self._set_data({})
        
    def get_info(self, query):
        #get the question
        query_lower = query.lower()
        
        #Check if there is something in the file related to question
        for title, info in self.data.items():
            if title.lower() in query_lower:
                return info
        return None
 
class PromptManager:
    def __init__(self):
        """
        template (str) : Basic template for a prompt to utilize the giving information
        """
        self.template = """
        You are an AI assistant specialized in answering questions about the game of Subnautica (and its official sequel, Subnautica: Below Zero). Your mission is to be a friendly, enthusiastic, and highly accurate guide to the world of Planet 4546B.

        I have retrieved the following verified information from a trusted source:
        ---
        Title: {title}
        Info: {info_text}
        URL: {url}
        ---

        Using ONLY the information provided above, please answer the user's question. If the provided information is insufficient to answer the question, state that you can't find the answer in the provided data.

        Maintain a cheerful, helpful, and optimistic tone, as if you're excited to share your knowledge of this incredible underwater world! Feel free to use encouraging language and an occasional exclamation point.

        Do not invent or embellish any details. Do not use any information that is not explicitly in the provided context. If a question is outside the scope of Subnautica or you cannot find an answer in the provided text, politely and cheerfully state that you can only answer questions related to the official games.

        User's Question: {question}
        Answer:
        """
    def create_history_aware_query(self, chat_history : list, user_question : str):
        history_str = "\n".join([
            f"{h['role'].capitalize()}: {h['parts'][0]}"
            for h in chat_history if h['role'] in ['user', 'model']
        ])
        
        template = """
        Given the following conversation and a follow-up question, please rephrase the follow-up question to be a standalone question.
        
        Chat History:
        {chat_history}
        
        Follow Up Input: {question}
        
        Standalone question:
        """
        
        return template.format(chat_history=history_str, question=user_question)
        
    def create_prompt(self, question : str, retrieved_info : str):
        title = retrieved_info.get('title', 'N/A') if retrieved_info else 'N/A'
        info_text = retrieved_info.get('summary', retrieved_info.get('content', 'No information found.')) if retrieved_info else 'No information found.'
        url = retrieved_info.get('url', 'N/A') if retrieved_info else 'N/A'

        return self.template.format(
            title=title,
            info_text=info_text,
            url=url,
            question=question
        )
        