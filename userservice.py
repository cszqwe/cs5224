class UserService():
    def __init__(self, dbManager):
        self.dbManager = dbManager
    
    def registerUser(self, userId, userMetadata):
        self.dbManager.insertUser(userId, userMetadata)

    def getUser(self, userId):
        return self.dbManager.getUser(userId)