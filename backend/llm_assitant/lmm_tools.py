# Custom Imports
from db_tools.data_access import UserDataAccessor

class LLM_Tools:
    def __init__(self):
        self.given_query = None
        self.tool_call = None
        self._TDA = UserDataAccessor()
        self.result_dict = dict()
        
    def update_tools_status(self, new_query : str, called_tool : str):
        self.given_query = new_query
        self.tool_call = called_tool
        
    def fetch_results(self):
        return self.result_dict or None
        
    def _tuple_to_dict(self, result_to_format : list) -> dict:
        FIELDS = ["pageid", "title", "fullurl", "extract", "thumbnail"]

        formatted = []
        for record in result_to_format:
            if len(record) != len(FIELDS):
                raise ValueError("Field mismatch in DB result")
            formatted.append(dict(zip(FIELDS, record)))

        return formatted
            
    def _clean_input_to_keywords(self, input_str : str) -> set:
        set_clean_input =  set()
        for word in input_str.strip().split():
            if len(word) > 3:
                set_clean_input.add(word)
                
        return set_clean_input
    
    def _search_by_keywords(self, query : str):
        #Creates keywords to search from
        keywords = self._clean_input(query)
        if keywords is None:
            return None
        
        #Queries DB for results
        found_results = self._TDA.search_for_similer_title(list(keywords))
        self.result_dict = self._tuple_to_dict(found_results)
        
    def _extract_page_ids(self) -> set:
        page_ids = set()
        for page in self.result_dict:
            page_ids.add(page["pageid"])
            
        return page_ids
            
    def _add_fields_to_dict(self, records : list, page_ids : set):
        CATEGORY_FIELDS = ["categories"]
        SECTIONS_FIELDS = ["pageid", "toclevel", "level", "line", "fromtitle", "anchor", "linkanchor"]
        
        #Determine who is adding
        dict_formatted_result = dict()
        if len(records[0]) == len(CATEGORY_FIELDS):
            #Add category
            i = 0
            for record in records:
                if record[0] == page_ids[i]:
                    self.result_dict[page_ids[i]] = {"categorgies" : record}
                    
        elif len(record[0]) == len(SECTIONS_FIELDS):
            #Add sections
            i = 0
            for record in records:
                if record[0] == page_ids[i]:
                        self.result_dict[page_ids[i]] = {"sections" : record}
    
    def _in_depth_search(self, query):
        try:
            #Get keywords from query + extract page ids
            self._search_by_keywords(query)
            set_page_ids = self._extract_page_ids()
            
            #Search for categories of the page
            found_results = self._TDA.get_page_categories(set_page_ids)
            self._add_fields_to_dict(found_results, set_page_ids)
            
            #Search for sections of the page
            found_results = self._TDA.get_page_sections(set_page_ids)
            self._add_fields_to_dict(found_results, set_page_ids)
            
        except Exception as e:
            print(f"An error occurred: {e}")

    def use_tool(self):
        #Determine the tool called
        if self.tool_call == "SEARCH_BY_KEYWORD":
            self._search_by_keywords(self.given_query)
            
        elif self.tool_call == "IN_DEPTH_SEARCH":
            self._in_depth_search(self.given_query)
            
        #Return None if no tool is called
        elif self.tool_call == "NO_TOOL":
            self.result_dict.clear()