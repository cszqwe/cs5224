# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
from pytrends.request import TrendReq
import socket
import json
import redis
import uuid
import pymysql    
import configparser

parser = configparser.ConfigParser()
parser.read("config.txt")
host = parser.get("config", "db_host")
user = parser.get("config", "db_user")
password = parser.get("config", "db_password")
name = parser.get("config", "db_name")
db = pymysql.connect(host=host, user=user, password=password, database=name)
cursor = db.cursor()
print(cursor)
cursor.execute("show tables;")
result = cursor.fetchone()
print(result)
hostName = socket.gethostname()
serverPort = 8080
pytrends = TrendReq(hl='en-US', tz=360)
r = redis.StrictRedis(host='taptotagredis.riupow.ng.0001.apse1.cache.amazonaws.com',
    port=6379, charset="utf-8", decode_responses=True)
# r.rpush('test1', '1')
# print(r.lpop('test1'))
# print(r.lpop('test1'))
class MyServer(BaseHTTPRequestHandler):
    def do_POST(self):
        requestPath = self.path
        print(self.path)
        if requestPath == "/register":
            self.handleRegister()
        if requestPath == "/match":
            self.handleMatch()
        if requestPath == "/gettag":
            self.handleGetTag()
        self.send_response(404)

    def handleRegister(self):
        # TODO: Write the userId into the database
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        print(post_body)
        parsedRequst = json.loads(post_body)
        userId = parsedRequst['userId']
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = json.dumps({'status' : 'successful'})
        self.wfile.write(bytes(response, encoding='utf8'))

    def handleMatch(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        print(post_body)
        parsedRequst = json.loads(post_body)
        userId = parsedRequst['userId']
        tag = parsedRequst['tag']
        # TODO: Update user searching history
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        # Search whether there is a matched session for this tag.
        sessionId = r.lpop(tag)
        if sessionId == None:
            sessionId = str(uuid.uuid1())
            r.rpush(tag, sessionId)
        else:
            sessionId = str(sessionId)
        response = json.dumps({'sessionId' : sessionId})
        self.wfile.write(bytes(response, encoding='utf8'))

    def handleGetTag(self):
        # TODO: Take use of pytrends, to make the random input string matches to a tag
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        print(post_body)
        parsedRequst = json.loads(post_body)
        input = parsedRequst['input']
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = json.dumps({'tag' : input})
        self.wfile.write(bytes(response, encoding='utf8'))

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
