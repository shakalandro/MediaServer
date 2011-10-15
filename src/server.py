'''
Created on Oct 14, 2011

@author: shakalandro
'''

import os
import sys
import subprocess
import socket
import BaseHTTPServer
import tempfile
#import vlc
from django import template
from django.conf import settings
settings.configure()


def get_index(path='..', template_path='src/server.html'):
    movie_files = ['avi', 'mpg', 'wmv', 'mp4', 'mov', 'mkv', 'flv', 'rm', 'dv']
    audio_files = ['mp3', 'wav']
    t = template.Template(open(template_path, 'r').read())
    c = template.Context({
        'Movies': filter(lambda x: os.path.splitext(x)[1][1:] in movie_files, os.listdir(path)),
        'Music': filter(lambda x: os.path.splitext(x)[1][1:] in audio_files, os.listdir(path))
    })
    return t.render(c)


class VLCProcess(subprocess.Popen):
    def __init__(self, *args):
        self.instr = tempfile.mkstemp()[0]
        self.outstr = tempfile.mkstemp()[0]
        super(VLCProcess, self).__init__(*args, stdout=self.outstr, stderr=self.outstr,
                                         stdin=self.instr)
    
    def get_out(self):
        return self.outstr.read()

    def put_in(self, val):
        self.instr.write(val)

    @staticmethod
    def Make(args_list):
        command = VLCProcess.VlcCommand()
        print list([command]) + args_list
        return VLCProcess(list([command]) + args_list)

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
            vlc = VLCProcess.Make(['-I', 'rc', 'test/data/2.avi', '--sout',
                                   '#standard{access=http,mux=avi,dst=localhost:8888}'])
            self.processes[self.client_address] = vlc
            self.wfile.write('New process created: 8888')
        return
    
    def do_GET(self):
        client_host, client_port = self.client_address
        print 'Serving %s to %s:%s' % (self.path, client_host, client_port)
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(get_index('/Users/shakalandro/Movies'))
        
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
        server.server_close()
        print 'shutting down'


if __name__ == '__main__':
    main()
        