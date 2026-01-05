from datetime import datetime

class User:
    def __init__(self, userID : int, name : str, username : str, convoID : int):
        self.userID = userID
        self.name = name
        self.username = username
        self.conversationID = convoID
        self.LoginAt = datetime.now()
        self.LogoutAt = None
        