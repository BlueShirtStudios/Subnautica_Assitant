CONFIGS = [
    { 
        "api": "https://subnautica.fandom.com/api.php",
        "output_path": "subnautica_wiki.jsonl",
        "params": {
                "action": "query",
                "format": "json",
                "prop": "info|extracts|pageimages|categories|sections|images",
                "inprop": "url",
                "generator": "allpages",
                "explaintext": True,   #no HTML, plain text
                "piprop": "thumbnail",
                "clshow": "!hidden",   #only visible categories
                "cllimit": "max",
                "gaplimit": "10"       #number of pages per batch
            }
    }
    
]