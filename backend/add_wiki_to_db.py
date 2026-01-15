import json
import time
from pathlib import Path
from db_tools.db_manager import Database_Manager
from knowledge_base.log_actions import Logger

INSERT_INTO_PAGES = """
    INSERT INTO pages
    (pageID, title, fullurl, extract, thumbnail)
    VALUES
    (%s, %s, %s, %s, %s)
"""

INSERT_INTO_CATEGORIES = """
    INSERT INTO categories
    (pageID, category_name)
    VALUES
    (%s, %s)
"""

INSERT_INTO_SECTIONS = """
    INSERT INTO sections
    (pageID, toclevel, level, line, number, index_number,
     fromtitle, byteoffset, anchor, linkanchor)
    VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

def clean(value):
    if value is None:
        return None
    if isinstance(value, str) and value.strip() == "":
        return None
    return value


def get_data_file() -> Path | None:
    try:
        ROOT = Path(__file__).resolve().parents[1]
        data_path = ROOT / "backend" / "data" / "subnautica_wiki.jsonl"

        if not data_path.exists():
            print("Data file not found:", data_path)
            return None

        return data_path

    except Exception as e:
        print(f"Error locating data file: {e}")
        return None

def insert_lines_into_db(data_path: Path):
    ROOT = Path(__file__).resolve().parents[1]

    log_path = ROOT / "backend" / "data" / "logs" / "add_wiki_to_db.log"
    if not log_path.exists():
        print("Creating log file")
        new_log_file = open(log_path, "a", encoding="utf-8")
        new_log_file.close()
        log_path = new_log_file
        
    logger = Logger(log_path, "Started Moving File to Database...")
    logger.initialize_logger("Started Migratations Process...")

    db_manager = Database_Manager()

    total_records_added = 0
    pages_processed = 0

    try:
        with db_manager as db:
            with open(data_path, "r", encoding="utf-8") as f:
                for raw_line in f:
                    try:
                        #Load each line and extract its info
                        line = json.loads(raw_line)
                        page_id = clean(line.get("pageid"))
                        title = clean(line.get("title"))
                        fullurl = clean(line.get("fullurl"))
                        extract = clean(line.get("extract"))
                        thumbnail = clean(line.get("thumbnail"))
                        
                        #Add to info to pages table
                        db.cursor.execute(
                        INSERT_INTO_PAGES,
                        (page_id, title, fullurl, extract, thumbnail))
                        
                        #Add info to category table
                        categories = line.get("category") or []
                        for category in categories:
                            category = clean(category)
                            db.cursor.execute(
                                INSERT_INTO_CATEGORIES,
                                (page_id, category))
                            
                            
                        #Add information to sections table
                        sections = line.get("sections") or []
                        for section in sections:
                            db.cursor.execute(
                                INSERT_INTO_SECTIONS, (
                                page_id,
                                clean(section.get("toclevel")),
                                clean(section.get("level")),
                                clean(section.get("line")),
                                clean(section.get("number")),
                                clean(section.get("index_number")),
                                clean(section.get("fromtitle")),
                                clean(section.get("byteoffset")),
                                clean(section.get("anchor")),
                                clean(section.get("linkanchor")),
                                ))
                            
                        #Commit changes to db
                        db.connection.commit()
                        
                        #Update log informations
                        pages_processed += 1
                        total_records_added += 1
                        logger.log_db_insert(pages_processed, title, "page")
                        logger.progress_bar.update(1)
                        time.sleep(0.25)

                    except Exception as e:
                        db_manager.connection.rollback()
                        logger.log_db_error_insert(pages_processed, e)
                        
                #Display when transfer is complete + log it
                logger.finish_log("Finished adding wiki data to database", total_records_added)
                print("Migration to db is done.")
    
    except json.JSONDecodeError as e:
        logger.log_json_error(page_id, pages_processed, e) 

    except Exception as e:
        logger.log_unexpected_error(e)

if __name__ == "__main__":
    data_file = get_data_file()
    if data_file:
        insert_lines_into_db(data_file)
