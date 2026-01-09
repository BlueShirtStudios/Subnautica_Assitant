import psycopg2
from psycopg2 import Error

from db_secrect import ALT_user_db

class Database_Manager:
    def __init__(self):
        self.connection = None
        self.cursor = None
        
    def connect_to_db(self):
        try:
            self.connection = psycopg2.connect(
                user=ALT_user_db["user"],
                password=ALT_user_db["password"],
                host=ALT_user_db["host"],
                port=ALT_user_db["port"],
                database=ALT_user_db["database"]
            )
            
            self.cursor = self.connection.cursor()
            print("Connected to DB")
        
        except (Exception, Error) as error:
            print(f"Error while connecting to PostgreSQL: {error}")
            
    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("PostgreSQL connection closed.")
        
    def __enter__(self):
        try:
            self.connect_to_db()
            return self
        except ConnectionError:
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()
        return False