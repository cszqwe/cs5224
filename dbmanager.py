import pymysql

class DbManager():
    def __init__(self, host, user, password, database):
        self.db = pymysql.connect(host=host, user=user, password=password, database=database)
        self.cursor = self.db.cursor()
    
    def createTables(self):
        self.cursor.execute("show tables;")
        result = self.cursor.fetchone()
        if result == None:
            self.cursor.execute("CREATE TABLE User ( UserId varchar(255), Metadata varchar(255));")
            self.cursor.execute("CREATE TABLE MatchRecord ( UserId varchar(255), Tag varchar(255));")

    def showTables(self):
        self.cursor.execute("show tables;")
        result = self.cursor.fetchone()

    def insertUser(self, userId, userMetaData):        
        self.cursor.execute("""INSERT INTO User(UserId,
         Metadata)
         VALUES ("%s", "%s")""" % (userId, userMetaData))
        result = self.cursor.fetchone()

    def getUser(self, userId):
        self.cursor.execute("SELECT * FROM User WHERE UserId=\"%s\"" % (userId))
        result = self.cursor.fetchone()
        return result[0], result[1]

    def insertMatchRecord(self, userId, tag):        
        self.cursor.execute("""INSERT INTO MatchRecord(UserId,
         Tag)
         VALUES ("%s", "%s")""" % (userId, tag))
        result = self.cursor.fetchone()
