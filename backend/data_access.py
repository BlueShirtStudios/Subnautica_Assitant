from db_manager import Database_Manager
from psycopg2 import ProgrammingError, IntegrityError, OperationalError, DataError, DatabaseError
from datetime import datetime
import bcrypt
import binascii
import user_template

#Query Templates
ADD_NEW_USER = "INSERT INTO users (password, name, surname, email, createdAt, lastActive, username) VALUES (%s, %s, %s, %s, %s, %s, %s)"

LOGIN_QUERY  = "SELECT userID, password, name FROM users WHERE username = %s"

CREATE_CONVERSATION_QUERY = "INSERT INTO conversations (userID, startedAt, EndedAt) VALUES (%s, %s, %s)"

SAVE_CONVERSATION_QUERY = "INSERT INTO "
               
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
            
    def login_user(self, username : str, password : str) -> user_template:
        with self.db as db:
            try:
                db.cursor.execute(LOGIN_QUERY, (username,))
                record = db.cursor.fetchone()
                
                if not record:
                    return None
                
                user_id, hashed_password, name = record
                if isinstance(hashed_password, str) and hashed_password.startswith('\\x'):
                    db_hash_bytes = binascii.unhexlify(hashed_password[2:])
                else:
                    db_hash_bytes = hashed_password
                
                if bcrypt.checkpw(password.encode(), db_hash_bytes):
                    convoID = self.create_conversation_record(user_id)
                    User = user_template(user_id, name, username, convoID)
                    return User
                
                else:
                    return None
                
            except ProgrammingError as e:
                print(f"An error occured during run: {e}")
                raise
            
    def create_conversation_record(self, userID : int) -> int:
        currentTime = datetime.now()
        with self.db as db:
            try:
                db.cursor.execute(CREATE_CONVERSATION_QUERY, (userID, currentTime, None,))
                db.connection.commit()
                
            except ProgrammingError as e:
                db.connection.rollback()
                print(f"A programming error occured: {e}")
                
            except Exception as e:
                db.connection.rollback()
                print(f"An error occured: {e}")
            