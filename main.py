# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
from pickle import TRUE
from pytrends.request import TrendReq
import socket
import json
import redis

hostName = socket.gethostname()
serverPort = 8080
pytrends = TrendReq(hl='en-US', tz=360)
r = redis.Redis(host='taptotagredis.riupow.ng.0001.apse1.cache.amazonaws.com',
    port=6379)
r.rpush('test1', '1')
print(r.lpop('test1'))
print(r.lpop('test1'))
class MyServer(BaseHTTPRequestHandler):
    def do_POST(self):
        requestPath = self.path
        print(self.path)
        if requestPath == "/match":
            self.handleMatch()
        if requestPath == "/gettag":
            self.handleMatch()
        self.send_response(404)
        
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
        response = json.dumps({'sessionId' : '123'})
        self.wfile.write(bytes(response, encoding='utf8'))

    def handleGetTag(self):
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
