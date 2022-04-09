import configparser
import pymysql    
import redis

class RedisManager():
    def __init__(self, host, port):
        self.r = redis.StrictRedis(host=host, port=port, charset="utf-8", decode_responses=True)
        
    def lpop(self, key):
        return self.r.lpop(key)

    def rpush(self, key, value):
        self.r.rpush(key, value)