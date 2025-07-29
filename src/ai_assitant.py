import google.generativeai as genai
import os

class AI_Assitant:
    def __init__(self, api_key: str = "GEMINI API KEY", prompt : str = None, question : str = None):
        self.api_key = api_key
        self.prompt = prompt
        self.question = question
        self.question = question

    def _setup_ai(self):
        #Sort API out
        api_key_name = "GEMINI_API_KEY"
        try:
            genai.configure(api_key=os.environ[api_key_name])
        except KeyError:
            print(f"Error: The '{api_key_name}' environment variable not set.")
            print("Please set it before running the script.")
            exit()
        
        """
        This part acts as a safety net that ensures an AI model will be chosen in the case that
        a model can not be reached
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
            return genai.GenerativeModel(available_model_name)
        else:
            print("Error: No suitable model found that supports 'generateContent' in your environment.")
            print("Please ensure you have access to Gemini 1.5 models (e.g., gemini-1.5-flash-00X) or gemini-pro.")
            print("Here are all models available to your API key that support generateContent:")
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    print(f"- {m.name}")
            exit()
            
    def get_answer(self, model_used, question):
        prompt = f"""
        You are an AI assistant specialized in answering questions about the game Subnautica (and Subnautica: Below Zero).
        Provide accurate, helpful, and concise answers based on game mechanics, lore, crafting, creatures, and locations.
        If a question is outside the scope of Subnautica or you don't know the answer, politely state that.

        Question: {question}
        Answer:
        """
        #Generate the response to the user
        try:
            response = model_used.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"An error occured during API call: {e}")
        return "Sorry. I am unable to do that currently. Please try again later."
    
    def start_ai(self):
        print("Welcome. I am your subnautica assistant")
        print("Ask me anything related to subnautica or subnautica below zero and I will do my best to provide you with an answer. Type 'Exit' if you wish to exit.")
        keep_Convo = True
        model_used = self._setup_ai()
        while keep_Convo:
            question = input("Enter your question: ")
            if question.upper() == "EXIT":
                print("See you soon. Safe swimming. Closing Assistant...")
                keep_Convo = False
            
            #Not exit; will proceed to give question
            print("Thinking....")
            response = self.get_answer(model_used, question)
            print(f"{response}")
    
        