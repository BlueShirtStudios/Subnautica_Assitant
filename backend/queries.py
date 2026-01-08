#Query Templates
#User login + create user
ADD_NEW_USER = """
                    INSERT INTO users 
                    (password, name, surname, email, createdAt, lastActive, username) 
                    VALUES 
                    (%s, %s, %s, %s, %s, %s, %s);
                    """

LOGIN_QUERY  = """
                    SELECT userID, password, name 
                    FROM users 
                    WHERE username = %s;"""
                    
#Conversation + Message Related Queries
CREATE_CONVERSATION_QUERY = """
                    INSERT INTO conversations 
                    (userID, startedAt, EndedAt) 
                    VALUES (%s, %s, %s) 
                    RETURNING conversationID;
                    """

SAVE_MESSAGE_QUERY = """
                    INSERT INTO messages 
                    (conversationID, role, content, sentAt) 
                    VALUES (%s, %s, %s, %s);
                    """

UPDATE_USER_LAST_ACTIVE = """
                    UPDATE users 
                    SET lastActive = %s 
                    WHERE userID = %s;
                    """

GET_RECENT_USER_CONVERSATIONS = """
                    SELECT conversationID 
                    FROM conversations 
                    WHERE userID = %s  
                    ORDER BY startedAt DESC
                    LIMIT 5;
                    """

GET_RECENT_USER_MESSAGES = """
                    SELECT messageID, role, content 
                    FROM messages 
                    WHERE conversationID = ANY(%s)
                    ORDER BY conversationID DESC, sentAt DESC
                    LIMIT 6
                    """
               