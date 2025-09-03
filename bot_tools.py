import json
import os
from collections import defaultdict

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
        
        with open(self.file_path, "r", encoding="utf8") as file:
            for line in file:
                #Add whole file to data
                entry = json.loads(line)
                self.data.append(entry)
                
                #Build Index
                title = entry.get("title", "").lower()
                for word in title.split():
                    self.index[word].append(entry)
        

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