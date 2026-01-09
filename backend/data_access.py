from db_manager import Database_Manager
from psycopg2 import ProgrammingError, IntegrityError, OperationalError, DataError, DatabaseError
from datetime import datetime
import bcrypt
import binascii

#Custom Imports
from user_template import User
import queries as q
class UserDataAccessor:
    def __init__(self):
        self.db = Database_Manager()
        self.db.connect_to_db()
        
    def add_new_user(self, username : str, password : str, name : str, surname : str, email : str):
        with self.db as db:
            password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            current_time = datetime.now()
            try:
                db.cursor.execute(q.ADD_NEW_USER, (password, name, surname, email, current_time, current_time, username,))
                db.connection.commit()
                
            except ProgrammingError as e:
                db.connection.rollback()
                print(f"A programming error occured: {e}")
                
            except Exception as e:
                db.connection.rollback()
                print(f"An error occured: {e}")
            
    def login_user(self, username : str, password : str) -> User:
        with self.db as db:
            try:
                db.cursor.execute(q.LOGIN_QUERY, (username,))
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
                    user_instance = User(user_id, name, username, convoID)
                    return user_instance
                
                else:
                    return None
                
            except ProgrammingError as e:
                print(f"An error occured during run: {e}")
                raise
            
    def create_conversation_record(self, userID : int) -> int:
        currentTime = datetime.now()
        with self.db as db:
            try:
                db.cursor.execute(q.CREATE_CONVERSATION_QUERY, (userID, currentTime, None,))
                db.connection.commit()
                conversation_id = db.cursor.fetchone()[0]
                return conversation_id
                
            except ProgrammingError as e:
                db.connection.rollback()
                print(f"A programming error occured: {e}")
                
            except Exception as e:
                db.connection.rollback()
                print(f"An error occured: {e}")
                
                
    def add_new_message(self, convoID : int, content : str, role : str):
        sentAt = datetime.now()
        with self.db as db:
            try:
            
                db.cursor.execute(q.SAVE_MESSAGE_QUERY, (convoID, role, content, sentAt,))
                db.connection.commit()
        
            except ProgrammingError as e:
                    db.connection.rollback()
                    print(f"A programming error occured: {e}")
                    
            except Exception as e:
                    db.connection.rollback()
                    print(f"An error occured: {e}")
                    
    def update_user_active_time(self, userID : int):
        currentTime = datetime.now()
        with self.db as db:
            try:
                db.cursor.execute(q.UPDATE_USER_LAST_ACTIVE, (currentTime, userID,))
                db.connection.commit()
            
            except ProgrammingError as e:
                db.connection.rollback()
                print(f"A programming error occured: {e}")
                        
            except Exception as e:
                db.connection.rollback()
                print(f"An error occured: {e}")
                
    def get_recent_conversationsIDs(self, userID : int) -> list[int]:
        with self.db as db:
            try:
                db.cursor.execute(q.GET_RECENT_USER_CONVERSATIONS, (userID,))
                records = db.cursor.fetchall()
                
                #Convert Tupled Records to Single list
                list_recent_convos = []
                for record in records:
                    list_recent_convos.append(record[0])
                    
                print(list_recent_convos)
                return list_recent_convos
            
            except ProgrammingError as e:
                db.connection.rollback()
                print(f"A programming error occured: {e}")
                        
            except Exception as e:
                db.connection.rollback()
                print(f"An error occured: {e}")
                
    def get_recent_messages(self, list_convoIDs : list) -> dict:
         with self.db as db:
            try:
                db.cursor.execute(q.GET_RECENT_USER_MESSAGES, (list_convoIDs,))
                records = db.cursor.fetchall()
                
                #Check if memory building is needed
                if records is None:
                    return None
                 
                #Convert into useable dictionary
                dict_conversations = {}
                i = 0
                for record in records:
                    convo_id = list_convoIDs[i]

                    if convo_id not in dict_conversations:
                        dict_conversations[convo_id] = {
                        "message_details": []
                    }

                    dict_conversations[convo_id]["message_details"].append({
                        "messageID": record[0],
                        "role": record[1],
                        "content": record[2]
                    })

                print(dict_conversations)
                return dict_conversations
                     
            except ProgrammingError as e:
                db.connection.rollback()
                print(f"A programming error occured: {e}")
                        
            except Exception as e:
                db.connection.rollback()
                print(f"An error occured: {e}")