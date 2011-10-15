'''
Created on Oct 14, 2011

@author: shakalandro
'''

import os
import sys
import subprocess
import socket
import BaseHTTPServer
import django.template

def get_index(path='../..'):
    return os.listdir(path)


class VLCProcess(subprocess.Popen):
    
    @staticmethod
    def Make(self, args_list):
        command = VLCProcess.VlcCommand()
        print command
        return VLCProcess(list(command, *args_list))

    @staticmethod
    def VlcCommand():
        linux = 'linux'
        mac = 'darwin'
        windows = 'win'
        cygwin = 'cygwin'
        platform = sys.platform
        if platform.startswith(linux):
            return 'vlc'
        elif platform.startswith(mac):
            return '/Applications/VLC.app/Contents/MacOS/VLC'
        elif platform.startswith(windows) or platform.startswith(cygwin):
            return 'vlc'


class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    processes = {}
    
    def fetch_process(self):
        vlc = None
        if self.client_address in self.processes:
            vlc = self.processes[self.client_address]
            self.wfile.write('Old process found: 8888')
        else:
            vlc[self.client_address] = VLCProcess(['-I', 'rc', '../test/data/2.avi', '-sout',
                                                   '#standard{access=http,mux=ts,dst=localhost:8888}'])
            self.wfile.write('New process created: 8888')
        return 
    
    def do_GET(self):
        client_host, client_port = self.client_address
        print 'Serving %s to %s:%s' % (self.path, client_host, client_port)
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write('Hello')
        vlc = self.fetch_process()
        
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        vlc = self.fetch_process()
    

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
        