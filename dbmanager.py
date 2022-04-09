import configparser
import pymysql    

class DbManager():
    def __init__(self, host, user, password, database):
        self.db = pymysql.connect(host=host, user=user, password=password, database=database)
        self.cursor = self.db.cursor()
    
    def createTables(self):
        self.cursor.execute("CREATE TABLE User ( UserId varchar(255), Metadata varchar(255));")
        result = self.cursor.fetchone()
        print(result)

    def showTables(self):
        self.cursor.execute("show tables;")
        result = self.cursor.fetchone()
        print(result)

    def insertUser(self, userId, userMetaData):        
        self.cursor.execute("""INSERT INTO User(UserId,
         Metadata)
         VALUES ("%s", "%s")""" % (userId, userMetaData))
        result = self.cursor.fetchone()
        print(result)

    def getUser(self, userId):
        self.cursor.execute("SELECT * FROM User WHERE UserId=\"%s\"" % (userId))
        result = self.cursor.fetchone()
        return result[0], result[1]
