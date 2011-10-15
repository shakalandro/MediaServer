'''
Created on Oct 14, 2011

@author: shakalandro
'''

import socket
import BaseHTTPServer


class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        client_host, client_port = self.client_address
        print 'Serving %s to %s:%s' % (self.path, client_host, client_port)
        self.send_header('Content-Type', 'text/html')
        self.wfile.write('Hello World!')
        
    def do_POST(self):
        self.send_header('Content-Type', 'text/html')
        self.wfile.write('Hello World!')

def main():
    port = 80
    try:
        server = BaseHTTPServer.HTTPServer(("", port), Handler)
    except:
        port = 8888
        server = BaseHTTPServer.HTTPServer(("", port), Handler)
    print 'Serving media on port %s' % port
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print 'shutting down'


if __name__ == '__main__':
    main()
        