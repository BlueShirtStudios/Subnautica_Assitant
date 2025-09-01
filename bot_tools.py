import json
import os

class Tools:
    def __init__(self, file_path : str ):
        self.file_path = file_path
        self.data = [{}]
        
    def _load_file(self):
        with open(self.file_path, "r", encoding="utf8") as file:
            for line in file:
                self.data.append(line)
                
    def search_by_keyword(self, keyword : str):
        for line in self.data:
            if 