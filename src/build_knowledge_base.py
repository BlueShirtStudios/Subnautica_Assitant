import requests
import json
import time
import os

""" MODULE DISCRIPTION
Builds a json file that the AI model will use to build its knowlegde about subnautica from
the official wiki page [https://subnautica.fandom.com/wiki/Subnautica_Wiki].
"""
class KnowledgeBuilder:
    """
    output_filename (str) : Name of JSON file that will contain the data
    api_url (str) : API Url of the website
    knowledge (dict) : Contain all the searched data
    items_to_scrape (List[str]) : Commen/Populer items users would look for 
    """
    def __init__(self, output_filename="knowledge_base.json"):
        self._output_file = os.path.join("src", output_filename)
        self._api_url = "https://subnautica.fandom.com/api.php"
        self._knowledge = {}
        self._items_to_scrape = [
            #Vehicles and Equipment
            "Seamoth", "Cyclops", "Prawn Suit", 
            "Mobile Vehicle Bay",
    
            #IMO Needed Resources
            "Titanium", "Copper Ore", "Lead",
            "Plasteel Ingot",
            "Aerogel",

            #Important Tools
            "Scanner", "Laser Cutter", "Stasis Rifle", "Habitat Builder",
    
            #Cool Creatures
            "Reaper Leviathan", "Gasopod", "Crashfish",
            "Sea Dragon Leviathan", "Ghost Leviathan",
            "Fauna of The Crater",
            "Fauna of Sector Zero",
            "Carnivores",
            "Herbivores",
            "Leviathan Class",


            #Biomes
            "Safe Shallows",
            "Kelp Forest",
            "Grassy Plateaus",
            "Mushroom Forest",
            "Jellyshroom Caves",
            "Blood Kelp Zone",
            "Grand Reef",
            "Bulb Zone",
            "Lost River",
            "Inactive Lava Zone",
            "Active Lava Zone",
            "Dunes",
            "Mountains"
        ]
        
    def _fetch_page_summary(self, page_title : str):  
        #Set parameters
        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts|info",
            "exchars": "1000",
            "explaintext": True,
            "inprop": "url",
            "titles": page_title
        }
          
        #Attempt to get information
        try:
            #Make request and save data
            response = requests.get(self._api_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            page_id = next(iter(data['query']['pages']))
            page_data = data['query']['pages'][page_id]
            
            #Check if page is found
            if page_id == -1:
                print(f"Warning: Page not found, {page_title}")
                return None
            
            #Summary of data
            summary = page_data.get('extract', 'No summary available')
            summary = summary.replace('\n', ' ').strip()
            
            if summary != 'No summary available':
                summary = summary.replace('\n', ' ').strip()
            
            #Return a dictionary with the extracted information
            return {
            "title": page_data.get('title'),
            "summary": summary,
            "url": page_data.get('fullurl')
        }
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for '{page_title}': {e}")
            return None
        
    def _fetch_page_content(self, page_title: str):
        #Set parameters
        params = {
            "action": "query",
            "format": "json",
            "prop": "revisions",
            "rvprop": "content", 
            "titles": page_title,
            "inprop": "url"
        }
        
        #Attempt to get information
        try:
            #Make request and save data
            response = requests.get(self._api_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            page_id = next(iter(data['query']['pages']))
            page_data = data['query']['pages'][page_id]
            
            #Check if page is found
            if page_id == '-1':
                print(f"Warning: Page not found for '{page_title}'")
                return None

            #Get all content from the revisions
            content = page_data['revisions'][0]['*']
            
            #Return a dictionary with the extracted information
            return {
                "title": page_data.get('title'),
                "content": content,
                "url": page_data.get('fullurl')
            }

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for '{page_title}': {e}")
            return None
        
    def build_and_save(self):
        print("Building knowledge base from Subnautica Wiki.....")
        
        for item in self._items_to_scrape:
            print(f"Fetching information for: {item}...")
            info = self._fetch_page_content(item)
            if info:
                self._knowledge[info['title']] = info
                print(f"-> Successfully added '{info['title']}' to the knowledge base.")
            else:
                print(f"-> Could not retrieve data for '{item}'. Skipping.")
                        
            time.sleep(5)
        
        with open(self._output_file, "w") as f:
            json.dump(self._knowledge, f, indent=4)
            
if __name__ == "__main__":
    builder = KnowledgeBuilder()
    builder.build_and_save()
