from db_tools.data_access import UserDataAccessor

class LLM_Tools:
    def __init__(self):
        self.given_query = None
        self.tool_call = None
        self._TDA = UserDataAccessor()
        
    def update_tools_status(self, new_query : str, called_tool : str):
        self.given_query = new_query
        self.tool_call = called_tool
        
    def tuple_to_dict(self, result_to_format : tuple) -> dict:
        FIELDS = ["pageid", "title", "fullurl", "extract", "thumbnail"]
        if len(result_to_format) != len(FIELDS):
            print("Field Mismatch, inserted data fields do not allign. ABORTING CONVERSION.")
            return None
        
        dict_formatted_results = dict
        for record in result_to_format:
            dict_formatted_results(zip(FIELDS, record))
            
        return dict_formatted_results
        
    def search_by_keywords(self, query : str) -> dict:
        #Creates keywords to search from
        keywords = set
        keywords = self._clean_input(query)
        if keywords is None:
            return None
        
        #Queries DB for results
        found_results = self._TDA.search_for_similer_title(keywords)
        
        return self.tuple_to_dict(found_results)
        
    def _clean_input(self, input_str : str) -> set:
        set_clean_input =  set
        for word in input_str.strip():
            if word > 3:
                set_clean_input.add(word)
                
        return set_clean_input
    
    def use_tool(self) -> dict:
        if self.tool_call == "SEARCH_BY_KEYWORD":
            dict_result = self.search_by_keywords(self.given_query)
            
            
        return dict_result