import configparser

class ConfigManager():
    def __init__(self, configFileName):
        configParser = configparser.ConfigParser()
        configParser.read(configFileName)
        self.dbHost = configParser.get("config", "db_host")
        self.dbUser = configParser.get("config", "db_user")
        self.dbPassword = configParser.get("config", "db_password")
        self.dbName = configParser.get("config", "db_name")
        self.redisHost = configParser.get("config", "redis_host")
        self.redisPort = configParser.get("config", "redis_port")
    
    def getDbConfig(self):
        return self.dbHost, self.dbUser, self.dbPassword, self.dbName
    
    def getRedisConfig(self):
        return self.redisHost, self.redisPort