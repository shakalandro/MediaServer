'''
Created on Oct 14, 2011

@author: shakalandro
'''

import socket
import BaseHTTPServer
import index


class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        client_host, client_port = self.client_address
        print 'Serving %s to %s:%s' % (self.path, client_host, client_port)
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(index.get_index())
        
    def do_POST(self):
        self.send_header('Content-Type', 'text/html')
        self.wfile.write('Hello World!')

def main():
    port = 80
    try:
        server = BaseHTTPServer.HTTPServer(("", port), Handler)
    except socket.error:
        port = 8888
        server = BaseHTTPServer.HTTPServer(("", port), Handler)
    print 'Serving media on port %s' % port
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print 'shutting down'


if __name__ == '__main__':
    main()
        