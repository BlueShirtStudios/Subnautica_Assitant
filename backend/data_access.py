from db_manager import Database_Manager
from psycopg2 import ProgrammingError, IntegrityError, OperationalError, DataError, DatabaseError
from datetime import datetime
import bcrypt
import binascii

#Query Templates
ADD_NEW_USER = "INSERT INTO users (password, name, surname, email, createdAt, lastActive, username) VALUES (%s, %s, %s, %s, %s, %s, %s)"

LOGIN_QUERY  = "SELECT userID, password FROM users WHERE username = %s"
               
class UserDataAccessor:
    def __init__(self):
        self.db = Database_Manager()
        self.db.connect_to_db()
        
    def add_new_user(self, username : str, password : str, name : str, surname : str, email : str):
        with self.db as db:
            password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            current_time = datetime.now()
            try:
                db.cursor.execute(ADD_NEW_USER, (password, name, surname, email, current_time, current_time, username,))
                db.connection.commit()
                
            except ProgrammingError as e:
                db.connection.rollback()
                print(f"A programming error occured: {e}")
                
            except Exception as e:
                db.connection.rollback()
                print(f"An error occured: {e}")
            
    def login_user(self, username : str, password : str) -> int:
        with self.db as db:
            try:
                db.cursor.execute(LOGIN_QUERY, (username,))
                record = db.cursor.fetchone()
                
                if not record:
                    return None
                
                user_id, hashed_password = record
                if isinstance(hashed_password, str) and hashed_password.startswith('\\x'):
                    db_hash_bytes = binascii.unhexlify(hashed_password[2:])
                else:
                    db_hash_bytes = hashed_password
                
                if bcrypt.checkpw(password.encode(), db_hash_bytes):
                    return user_id
                
                else:
                    return None
                
            except ProgrammingError as e:
                print(f"An error occured during run: {e}")
                raise