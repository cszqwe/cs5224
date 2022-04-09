import uuid

class MatchService():
    def __init__(self, dbManager, redis):
        self.dbManager = dbManager
        self.redis = redis    

    def doMatch(self, userId, tag):
        self.dbManager.insertMatchRecord(userId, tag)
        sessionId = self.redis.lpop(tag)
        if sessionId == None:
            sessionId = str(uuid.uuid1())
            self.redis.rpush(tag, sessionId)
        else:
            sessionId = str(sessionId)
        return sessionId        