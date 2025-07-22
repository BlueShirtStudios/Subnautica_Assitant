import google.generativeai as genai
import os
     
def subnuatica_AI_setup():
    api_key_name = "GEMINI_API_KEY"

    # Set up API key
    try:
        genai.configure(api_key=os.environ[api_key_name])
    except KeyError:
        print(f"Error: The '{api_key_name}' environment variable not set.")
        print("Please set it before running the script.")
        exit()
        

    available_model_name = None
    print("Attempting to list available models and select a suitable one...")

    preferred_prefixes = ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']
    
    # Store models that meet criteria to pick the best later
    found_suitable_models = []

    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            for prefix in preferred_prefixes:
                if m.name.startswith(prefix):
                    found_suitable_models.append(m)
                    break # Found a match for this prefix, move to next model in list_models()

    # Now, sort and pick the best one.
    # A simple sorting strategy is to prioritize by the order in `preferred_prefixes`.
    for prefix in preferred_prefixes:
        for m in found_suitable_models:
            if m.name.startswith(prefix):
                available_model_name = m.name
                print(f"Prioritizing and using model: {available_model_name}")
                break # Found the highest priority model, exit outer loop
        if available_model_name:
            break # Exit if a suitable model was found

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
    
def get_subnautica_answer(model_used, question):
    prompt = f"""
    You are an AI assistant specialized in answering questions about the game Subnautica (and Subnautica: Below Zero).
    Provide accurate, helpful, and concise answers based on game mechanics, lore, crafting, creatures, and locations.
    If a question is outside the scope of Subnautica or you don't know the answer, politely state that.

    Question: {question}
    Answer:
    """
    
    #Generate the content
    try:
        response = model_used.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"An error occured during API call: {e}")
        return "Sorry. I am unable to do that currently. Please try again later."
    
def start_AI():
    print("Welcome. I am your subnautica assistant")
    print("Ask me anything related to subnautica or subnautica below zero and I will do my best to provide you with an answer. Type 'Exit' if you wish to exit.")
    keep_Convo = True
    model_used = subnuatica_AI_setup()
    while keep_Convo:
        question = input("Enter your question: ")
        if question.upper() == "EXIT":
            print("See you soon. Safe swimming. Closing Assistant...")
            keep_Convo = False
            
        #Not exit; will proceed to give question
        print("Thinking....")
        response = get_subnautica_answer(model_used, question)
        print(f"{response}")