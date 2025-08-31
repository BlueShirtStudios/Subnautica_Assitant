import requests
import json
import time

class Crawler:
    def __init__(self, api : str, output_path : str, params = dict):
        self.api = api
        self.output_path = output_path
        self.params = params
        self.session = "User-Agent: ALT_SubnauticaAssistant/1.2 (Student Project; contact blue.shirt.studios101@gmail.com)"
        self.seen_page_ids = set()
        self.pages_written = 0
        
    def get_api(self):
        return self.api

    def set_api(self, api: str):
        self.api = api

    def get_session(self):
        return self.session

    def set_session(self, session : str):
        self.session = session

    def get_output_path(self):
        return self.output_path

    def set_output_path(self, path: str):
        self.output_path = path
        
    def get_params(self):
        return self.params
    
    def set_params(self, params : dict):
        self.params = params
        
    def get_seen_page_ids(self):
        return self.seen_page_ids
        
    def get_pages_written(self):
        return self.pages_written
    
    def set_pages_written(self, pages_written : int):
        self.pages_written = pages_written
    
    def make_presence_known(self):
        self.session = requests.Session()
        self.session.headers.update({
           "User-Agent": "ALT_SubnauticaAssistant/1.2 (Student Project; contact blue.shirt.studios101@gmail.com)"
        })

    def add_seen_page(self, seenpage_id : int):
        self.get_seen_page_ids().add(seenpage_id)
        
    def increment_pages_written(self):
        self.set_pages_written(self.get_pages_written() + 1)
        
    def crawl_over_all(self, delay=0.5):
        with open(self.get_output_path(), "a", encoding='utf-8') as file:
            while True:
                res = self.get_session().get(
                        self.get_api(), 
                        params=self.get_params(), 
                        timeout = 30)
                res.raise_for_status()
                data = res.json()
                
                pages = data.get("query", {}).get("pages", {})
                for page_id_str, page in pages.items():
                    page_id = page.get("pageid")
                    if page_id in self.get_seen_page_ids():
                        continue
                
                self.add_seen_page(page_id)
                
                record = {
                    "pageid": page_id,
                    "title": page.get("title"),
                    "fullurl": page.get("fullurl"),
                    "extract": page.get("extract"),
                    "thumbnail": (page.get("thumbnail") or {}).get("source"),
                    "categories": [c["title"] for c in page.get("categories", []) if not c.get("hidden")]
                }
                
                file.write(json.dumps(record, ensure_ascii=False) + "\n")
                self.increment_pages_written()
                
                if "continue" in data:
                    self.get_params().update(data["continue"])
                    time.sleep(delay)
                else:
                    break
        print(f"Finished Crawling. Wrote {self.get_pages_written()} pages to {self.get_output_path()}")