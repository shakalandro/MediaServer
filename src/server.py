'''
Created on Oct 14, 2011

@author: shakalandro
'''

import socket
import BaseHTTPServer


class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_header('Content-type', 'text/html')
        self.wfile.write('Hello World!')
        
    def do_POST(self):
        self.send_header('Content-type', 'text/plain')
        self.wfile.write('Hello World!')

def main():
    try:
        PORT = 80
        server = BaseHTTPServer.HTTPServer(("", PORT), Handler)
        print 'Serving media on port %s' % PORT
        server.serve_forever()
    except socket.error:
        PORT = 8888
        server = BaseHTTPServer.HTTPServer(("", PORT), Handler)
        print 'Serving media on port %s' % PORT
        server.serve_forever()
    except KeyboardInterrupt:
        print '^c received, shutting down'

if __name__ == '__main__':
    main()
        