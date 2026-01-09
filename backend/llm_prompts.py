class LLM_Prompts_Manager:
    def __init__(self):
        pass
    
    def found_in_recent_chats(question : str, prev_llm_response : str) -> str:
        if question or prev_llm_response is None:
            return None
        
        return f"""
            The user has asked a question similar to one they asked recently.

            New user question:
            {question}

            Previous LLM response:
            {prev_llm_response}

            Instructions:
            1. Compare the new question with the previous one.
            2. Identify any new details or differences in the new question.
            3. Generate a **new, improved answer** incorporating what was already provided.
            4. Avoid copying the previous response word-for-word.
            5. Keep the answer clear and concise.

            Provide the updated response below:
                
        """