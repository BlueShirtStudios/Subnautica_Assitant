import json
import os
from collections import defaultdict
import requests

class Tools:
    def __init__(self, file_path : str ):
        self.file_path = file_path
        self.data = []
        self.index = defaultdict(list)
        self._load_file()
        
    def _load_file(self):
        if not os.path.exists(self.file_path):
            print("File not found.")
            exit()
            
        try:
            with open(self.file_path, "r", encoding="utf8") as file:
                for line in file:
                    #Add whole file to data
                    entry = json.loads(line)
                    self.data.append(entry)
                
                    #Build Index
                    title = entry.get("title", "").lower()
                    for word in title.split():
                        self.index[word].append(entry)
        except json.JSONDecodeError as e:
            return f"Error has occured: {e}"
        

    def search_by_keyword(self, line : str):
        search_result = []
        unique_results = set()
        
        for word in line.lower().split():
            if not word:
                continue
            
            if word in self.index:
                for entry in self.index[word]:
                    if entry.get("pageid") not in unique_results:
                        unique_results.add(entry.get("pageid"))
                        search_result.append({ 
                                          "pageid": entry.get("pageid", "N/A"), 
                                          "title": entry.get("title", "N/A"), 
                                          "fullurl": entry.get("fullurl", "N/A"),
                                          "thumbnail": entry.get("thumbnail", "N/A"),
                                          "categories": entry.get("categories", "N/A")})
                        
        return search_result
    
    def scan_history(self, chat_memory : list, question : str):
        query_key_words = set(question.lower().split())
        
        for entry in reversed(chat_memory):
            summary_text = entry.get("summary", '')
            searchable_text = summary_text.lower()
            
            is_relevant = False
            for word in query_key_words:
                if word in searchable_text:
                    is_relevant = True
                    break
                
        if is_relevant:
            return summary_text
            
        return None
    
    def formatEntry(self, question : str, response : str):
        combined_entry = {"user": question, "model": response}
        return combined_entry
               