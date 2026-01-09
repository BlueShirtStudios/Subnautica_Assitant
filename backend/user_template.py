from datetime import datetime

class User:
    def __init__(self, userID : int, name : str, username : str, convoID : int):
        #User Specific
        self.userID = userID
        self.name = name
        self.username = username
        
        #Conversation Details
        self.conversationID = convoID
        self.current_messageID = None
        self.recent_memory = [dict]
        
        #Time Details
        self.LoginAt = datetime.now()
        self.LogoutAt = None
        