# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
from pytrends.request import TrendReq
import socket
import json
import uuid
from config import ConfigManager
from dbmanager import DbManager
from redismanager import RedisManager

configManager = ConfigManager("config.txt")
dbHost, dbUser, dbPassword, dbName = configManager.getDbConfig()
dbManager = DbManager(dbHost, dbUser, dbPassword, dbName)
redisHost, redisPort = configManager.getRedisConfig()
hostName = socket.gethostname()
serverPort = 8080
pytrends = TrendReq(hl='en-US', tz=360)
redisInstance = RedisManager(redisHost, redisPort)

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
        sessionId = redisInstance.lpop(tag)
        if sessionId == None:
            sessionId = str(uuid.uuid1())
            redisInstance.rpush(tag, sessionId)
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
