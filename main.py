# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
from pickle import TRUE
import time
import socket
import json

hostName = socket.gethostname()
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

    def do_POST(self):
        requestPath = self.path
        print(self.path)
        if requestPath == "/tagtochat":
            self.handleTagToChat()
        self.send_response(404)
        
    def handleTagToChat(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        print(post_body)
        parsedRequst = json.loads(post_body)
        userId = parsedRequst['userId']
        tag = parsedRequst['tag']
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = json.dumps({'matchedUserId' : '123', 'matchedStatus' : 'FINISHED'})
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
