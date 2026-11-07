from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import time
import threading

class MyHTTPServer(HTTPServer):
    def __init__(self, address, handler, state):
        super().__init__(address,handler)
        
        self.STATE = state
        self.authorization_code = None
        self.auth_error = None
        self.my_event = threading.Event()

class server_handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        parsed_path = urlparse(path)
        params = parse_qs(parsed_path.query)
        callback = parsed_path.path
        current_state = params.get('state',[None])[0]
        error = params.get('error',[None])[0]
        authorization_code = params.get('code', [None])[0]

        if callback != '/callback':
            return

        if error is not None:
            self.server.auth_error = error
            self.server.my_event.set()
            self.send_response(200)
            self.end_headers()
        elif current_state is None:
            self.server.auth_error = "failed big dawg"
            self.server.my_event.set()
            self.send_response(200)
            self.end_headers()
        elif self.server.STATE != current_state:
            self.server.auth_error = "failed big dawg"
            self.server.my_event.set()
            self.send_response(400)
            self.end_headers()
        elif authorization_code is None:
            self.server.auth_error = "failed big dawg"
            self.server.my_event.set()
            self.send_response(200)
            self.end_headers()
        else:
            self.server.authorization_code = authorization_code
            self.server.my_event.set()
            self.send_response(200)
            self.end_headers()
        
    pass

def run(httpd):
    httpd.serve_forever()

