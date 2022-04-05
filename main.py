# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
from pytrends.request import TrendReq
import socket
import json
import boto3
import redis
import uuid
import mysql.connector
import os

ENDPOINT="tagtochatdatabase.ci7oh0wmc7lp.ap-southeast-1.rds.amazonaws.com"
PORT="3306"
USER="admin"
REGION="ap-southeast-1"
DBNAME="tagtochatdatabase"
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

#gets the credentials from .aws/credentials
session = boto3.Session(profile_name='default')
client = session.client('rds')

token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)

try:
    conn =  mysql.connector.connect(host=ENDPOINT, user=USER, passwd=token, port=PORT, database=DBNAME, ssl_ca='SSLCERTIFICATE')
    cur = conn.cursor()
    cur.execute("""SELECT now()""")
    query_results = cur.fetchall()
    print(query_results)
except Exception as e:
    print("Database connection failed due to {}".format(e))          
                


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
