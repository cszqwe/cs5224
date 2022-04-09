# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import json
from config import ConfigManager
from dbmanager import DbManager
from redismanager import RedisManager
from userservice import UserService
from matchservice import MatchService
from tagservice import TagService

configManager = ConfigManager("config.txt")
dbHost, dbUser, dbPassword, dbName = configManager.getDbConfig()
dbManager = DbManager(dbHost, dbUser, dbPassword, dbName)
dbManager.createTables()
redisHost, redisPort = configManager.getRedisConfig()
hostName = socket.gethostname()
serverPort = 8080
redisInstance = RedisManager(redisHost, redisPort)
userService = UserService(dbManager)
matchService = MatchService(dbManager, redisInstance)
tagService = TagService()

class TagToTapServer(BaseHTTPRequestHandler):
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
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        parsedRequst = json.loads(post_body)
        userId = parsedRequst['userId']
        metaData = parsedRequst['userMetadata']
        userService.registerUser(userId, metaData)
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
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        sessionId = matchService.doMatch(userId, tag)
        response = json.dumps({'sessionId' : sessionId})
        self.wfile.write(bytes(response, encoding='utf8'))

    def handleGetTag(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        print(post_body)
        parsedRequst = json.loads(post_body)
        input = parsedRequst['input']
        tag = tagService.getTag(input)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = json.dumps({'tag' : tag})
        self.wfile.write(bytes(response, encoding='utf8'))

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), TagToTapServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
