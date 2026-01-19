class LLM_Prompts_Manager:
    def __init__(self):
        pass
    
    def found_in_recent_chats(self, question : str, prev_llm_response : str) -> str:
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
        
    def determine_tool_call(self, question : str) -> str:
        if question in None:
            return None
        
        return f"""
                Interpreate the user's question and decide if a tool call is needed, repsond in all capital letters with the tool name.
                
                User Question:
                {question}
                
                Instructions:
                1. Look at the user's question.
                2. Decide whether a tool is needed.
                3. Respond with NO_TOOL or the tool name chosen.
                4. See given examples for call examples.
                
                Look at an example:
                    -For generel questions, respond with NO_TOOL. For example: 
                    Question: How is your day?
                    Respond: NO_TOOL
                    
                    -For any factual questions, respond with with tool you want to call, for example:
                    Question: What are animals found in subnautica?
                    Respond: SEARCH_BY_KEYWORD
                    
                    Question: How to craft a seamoth?
                    Respond: SEARCH_BY_KEYWORD
    
        """
        
        
    def info_on_question_found(self, question : str, found_info : str) -> str:
        if question in None:
            return None
        
        return f"""
            Based on the call you made, we found all relevant information.
            
            Question: {question}
            
            Found Results: {found_info}
            
            Instructions:
            1. Look at the question.
            2. Look at the provided results.
            3. Combine both and deliver a robust reponse that answers the correctly. 
    
        """