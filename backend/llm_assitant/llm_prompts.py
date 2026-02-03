class LLM_Prompts_Manager:
    def __init__(self):
        pass
    
    def found_in_recent_chats(self, question : str, prev_llm_response : str) -> str:
        if question is None or prev_llm_response is None:
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
        if question is None:
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
                    
                    -For any factual questions, respond with with a search tool you want to call, for example:
                    Question: What are animals found in subnautica?
                    Respond: SEARCH_BY_KEYWORD
                    
                    Question: How to craft a seamoth?
                    Respond: SEARCH_BY_KEYWORD
    
            """
        
    def info_on_question_found(self, question : str, found_info : str) -> str:
        if not question:
            return None
        
        return f"""
            Based on the call you made, we found all relevant information.
            
            Question: {question}
            
            Found Results: {found_info}
            
            Instructions:

            - Carefully read the question.
            - Analyze the retrieved information.
            - Use ONLY the provided information to answer the question.
            - If the information does not fully answer the question, state what is missing.
            - Respond clearly, concisely, and accurately.
            """
            
    def understand_knowledge_base(self) -> str:
        return"""
            This is how the knowledge base database looks. It consists of 3 tables:
            
            Table 1: pages
            Desc: This contains a page main info.
            Fields:
                - pageid : A unipue ID for the page were we found the info.
                - title : The page title.
                - fullurl : URL for the page.
                - extract : Contain little or None information about the page.
                - thumbnail : Picture from the webpage.
                
            Table 2: categories
            Desc: This contains each category of a page.
            Fields:
                - id : Ignore.
                - pageid : A unipue ID for the page were we found the info, linking back to table 1 (pages).
                - categoriers : A list of each category where the page falls under.
                
            Table 3: sections
            Desc: Contains each section of a page
            Fields:
                - id : Ignore.
                - pageid : A unipue ID for the page were we found the info, linking back to table 1 (pages).
                - toclevel : Depth in the table of content (use this to understand hierachy of information).
                - level : The level of html heading.
                - line : The display title of the section.
                - number : Hieracrhical Section Number (use this to understand hierachy of information).
                - index_number : Ignore
                - fromtitle : Title of parent page.
                - byteoffset INTEGER,
                - anchor : Slug of the URL used to jump to that section.
                - linkAnchor : Slug of the URL used to jump to that section.

        """
        
        
    def summarize_current_message(self, msg_list : list) -> str:
        if msg_list is None:
            return None
        
        return f"""
            Summarize this interaction using the information provided:
            
            {msg_list}
        
            """
            
    def need_context(self, sum_msgs : str) -> str:
        if sum_msgs is None:
            return None
        
        return f"""
            To ensure the conversation stays on topic and accruate responses are given, we are
            refreshing your context. This is the last 10 messages between you and the user summarized.
            
            Summarized Version: {sum_msgs}
        """