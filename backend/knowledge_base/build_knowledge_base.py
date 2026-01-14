import requests
import json
import time
from log_actions import Logger

class Crawler:
    def __init__(self, api : str, output_path : str, params = dict):
        self.api = api
        self.output_path = output_path
        self.params = params
        self.session = requests.Session()
        self.session.headers.update({
           "User-Agent": "ALT_SubnauticaAssistant/1.2 (Student Project; contact blue.shirt.studios101@gmail.com)"
        })
        self.seen_page_ids = set()
        self.pages_written = 0
        self.logger = Logger("crawler.log")

    def add_seen_page(self, seenpage_id : int):
        self.seen_page_ids.add(seenpage_id)
        
    def increment_pages_written(self):
        self.pages_written += 1
        
    def get_sections(self, page_id : int):
        section_params = {
            "action": "parse",
            "pageid": page_id,
            "prop": "sections",
            "format": "json"
        }
        try:
            res = self.session.get(self.api,
                                   params=section_params,
                                   timeout=30)
            res.raise_for_status()
            
            try:
                data = res.json()
                sections = data.get("parse", {}).get("sections", [])
                return sections
            
            except json.JSONDecodeError as e:
                print(f"JSONDecodeError for page {page_id}: {e}")
                print(f"Response status: {res.status_code}, content: {res.text[:100]}...")
                return []
        
        except requests.exceptions.RequestException as e:
            print(f"Error with fetching sections for page: {page_id}: {e}")
               
    def crawl(self, delay=0.5):
        self.logger.initialize_logger("Started Crawl...")
        
        with open(self.output_path, "a", encoding='utf-8') as file:
            while True:
                res = self.session.get(
                        self.api, 
                        params=self.params, 
                        timeout = 30)
                res.raise_for_status()
                data = res.json()
                
                pages = data.get("query", {}).get("pages", {})
                for page_id_str, page in pages.items():
                    page_id = page.get("pageid")
                    if page_id in self.seen_page_ids:
                        continue
                    self.add_seen_page(page_id) 
                     
                    section_data = self.get_sections(page_id) 
                    record = {
                        "pageid": page_id,
                        "title": page.get("title"),
                        "fullurl": page.get("fullurl"),
                        "extract": page.get("extract") or self.get_missing_extract(page.get("title")),
                        "thumbnail": (page.get("thumbnail") or {}).get("source"),
                        "categories": [c["title"] for c in page.get("categories", []) if not c.get("hidden")],
                        "sections": section_data
                    }
                
                    try:
                        file.write(json.dumps(record, ensure_ascii=False) + "\n")
                        file.flush()
                        self.increment_pages_written()
                        self.logger.progress_bar.update(1)
                        self.logger.log_dump(page_id, record["title"] )
                    except Exception as e:
                        self.logger.log_error(page_id, e)
                        
                
                if "continue" in data:
                    self.params.update(data["continue"])
                    time.sleep(delay)
                else:
                    break
                    
        print(f"Finished Crawling. Wrote {self.pages_written} pages to {self.output_path}")
        
    def get_missing_extract(self, title : str):
        extract_params = {
            "action": "query",
            "format": "json",
            "titles": title,
            "prop": "extracts",
            "explaintext": True
        }
        try:
            res = self.session.get(self.api, params=extract_params, timeout=30)
            res.raise_for_status()
            data = res.json()
            pages = data.get("query", {}).get("pages", {})
            for page_id, page in pages.items():
                return page.get("extract", "")
            
        except requests.exceptions.RequestException as e:
            print(f"Error with fetching extract for {title} : {e}")
            return ""     