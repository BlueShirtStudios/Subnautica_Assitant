import google.generativeai as genai
import os

""" MODULE DESCRIPTION
An AI assitant that can quickly help users with any question they need an answer with. Related functions for the API setup and,
fallback net and conversation will be here. GEMINI AI model used in this code, I am unsure of the model due to fallback method
"""
class AI_Assitant:
    """
    api_key (str) : The API I am using for the GEMINI Model
    prompt (str) : Prompt the AI recieves to know how to answer the questions
    question (str) : Question from the user the AI needs to answer
    converation_history (list[dict]) : List of past conversations of current session
    response (str) : Response of the AI
    """
    def __init__(self, api_key_name : str = None, prompt : str = None, question : str = None, response : str = None,
                 conversation_history : list[dict] = None):
        self._api_key_name = api_key_name
        self._prompt = prompt
        self._question = question
        self._response = response
        self._conversation_history = conversation_history if not None else []
        
        #Add prompt to history
        if self._prompt:
            self._conversation_history.insert(0, {'role': 'user', 'parts': self._prompt})
        
    def _set_prompt(self):
        self.prompt = """You are an AI assistant specialized in answering questions about the game Subnautica. Your mission is to be a friendly and enthusiastic guide to the world of Planet 4546B.
        When a user asks a question, dive deep and provide a comprehensive, detailed answer. Explain game mechanics, crafting recipes, creature behaviors, lore, and locations with as much rich detail as possible.
        Maintain a cheerful, helpful, and optimistic tone, as if you're excited to share your knowledge of this incredible underwater world! Feel free to use encouraging language and an occasional exclamation point.
        If a question falls outside of the scope of Subnautica or you do not know the answer, politely and cheerfully state that you can only answer questions related to the games.
        """
        
    def _set_api_key_name(self):
        self.api_key_name = "GEMINI_API_KEY"
        
    def _set_question(self, new_question : str):
        self.question = new_question
        
    def _set_response(self, new_respnse : str):
        self.response = new_respnse
        
    def get_prompt(self):
        return self.prompt
    
    def get_question(self):
        return self.question
    

    def _setup_ai(self):
        #Sort API out
        self._set_api_key_name()
        try:
            genai.configure(api_key=os.environ[self.api_key_name])
        except KeyError:
            print(f"Error: The '{self.api_key_name}' environment variable not set.")
            print("Please set it before running the script.")
            exit()
        
        """
        This part acts as a safety net that ensures an AI model will be chosen in the case that
        a model can not be reached.
        """
        available_model_name = None
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
        
            #Intailze the history for this session
            self.conversation_history = []
            return genai.GenerativeModel(available_model_name)
        else:
            print("Error: No suitable model found that supports 'generateContent' in your environment.")
            print("Please ensure you have access to Gemini 1.5 models (e.g., gemini-1.5-flash-00X) or gemini-pro.")
            print("Here are all models available to your API key that support generateContent:")
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    print(f"- {m.name}")
            exit()
        
    def _add_user_question(self, user_question : str):
        self._set_question(user_question)
        self.conversation_history.append({'role': 'user', 'parts' : [self.question]})
        
    def _add_ai_response(self, response : str):
        self._set_response(response)
        self.conversation_history.append({'role' : 'model', 'parts' : [self.response]})
            
    def get_answer_of_question(self, model_used, question):
        #Add question with details to history list
        self._add_user_question(question)
        
        #Attempt to construct a response
        try:
            response = model_used.generate_content(self.conversation_history)
            
            #Add AI response to history list + set new
            self._add_ai_response(response.text.strip())
            self._set_response(response.text.strip())
            return response.text.strip()
        
        except Exception as e:
            print(f"An error occured during API call: {e}")
            return "Sorry. I am unable to do that currently. Please try again later."
    
    def start_ai(self):
        print("---------------------------------------")
        print("Welcome. I am your subnautica assistant")
        print("Ask me anything related to subnautica or subnautica below zero and I will do my best to provide you with an answer. Type 'Exit' or 'Bye' if you wish to leave.")
        print("---------------------------------------")
        
        #Intialize to prep for use
        keep_Convo = True
        model_used = self._setup_ai()
        list_leave_words = ["EXIT", "BYE"]
        
        #Begin the chat
        while keep_Convo:
            question = input("Enter your question: ")
            if question.upper() in list_leave_words:
                print("See you soon. Safe swimming. Closing Assistant...")
                keep_Convo = False
            
            #Proceed to give user answer as output
            print("Thinking....")
            response = self.get_answer_of_question(model_used, question)
            print(f"{response}")
    
        