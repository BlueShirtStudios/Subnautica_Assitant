import logging
from tqdm import tqdm

class Logger:
    def __init__(self, log_file : str, provided_desc : str):
        self.log_file = log_file
        self.log_format = "%(asctime)s [%(levelname)s] %(message)s"
        self.progress_bar = tqdm(total=None, desc=provided_desc)
        
    def initialize_logger(self, logger_start_message : str):
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format=self.log_format
        )
        logging.info(logger_start_message)
    
    def log_dump_page(self, pageid : int, title : str):
        logging.info(f"Dumped page {pageid}: {title}")
        self.progress_bar.update(1)
        
    def log_error_page(self, pageid : int, e : str):
        logging.error(f"Error fetching sections for page {pageid}: {e}")
        
    def log_db_insert(self, file_line : int, title : str, table_name):
        logging.info(f"Inserted Fields of Line {file_line}: {title} into {table_name}")
        
    def log_db_error_insert(self, file_line : int, e : str):
        logging.error(f"Error inserting line {file_line}: {e}")
        
    def finish_log(self, finsh_message : str, total_lines_added):
        logging.info(f"{finsh_message}, {total_lines_added}")
        print(f"{finsh_message}, {total_lines_added}") 
        
    def log_json_error(self, page_id : int, line : int, e : str):
        logging.error(f"AN JSON error Occurred During Writing on Page {page_id}, File Line {line}: {e}")
        
    def log_unexpected_error(self, e : str):
        logging.error(f"An unexpected error occured: {e}")