'''
Created on Oct 14, 2011

@author: shakalandro
'''

import cgi
import os
import sys
import daemon
import subprocess
import socket
import BaseHTTPServer
import tempfile
import threading
import re
import optparse
from django import template
from django.conf import settings
settings.configure()    


class PortBind(object):
        def __init__(self, num):
            self.num = str(num)
            self.used = False


class VLCProcess(subprocess.Popen):
    
    USED_PORTS = map(lambda x: PortBind(x), range(33433, 33433 + 10))
    port_in_use = None

    def __init__(self, *args):
        #self.instr = tempfile.mkstemp()[0]
        #self.outstr = tempfile.mkstemp()[0]
        #super(VLCProcess, self).__init__(*args, stdout=self.outstr, stderr=self.outstr,
        #                                 stdin=self.instr)
        super(VLCProcess, self).__init__(*args)
    
    def get_out(self):
        return self.outstr.read()

    def put_in(self, val):
        self.instr.write(val)

    @staticmethod
    def Make(path, args_list):
        command = VLCProcess.GetVlcCommand()
        args_list = VLCProcess.BuildArgs(path, args_list)
        return VLCProcess(list([command]) + args_list)

    @staticmethod
    def GetVlcCommand():
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

    @staticmethod
    def AllocatePort():
        VLCProcess.port_in_use = filter(lambda x: not x.used, VLCProcess.USED_PORTS)[0]
        VLCProcess.port_in_use.used = True
        return VLCProcess.port_in_use
    
    @staticmethod
    def FreePort():
        VLCProcess.port_in_use.used = False
        VLCProcess.port_in_use = None    
    
    @staticmethod
    def BuildArgs(path, data):
        file_name = os.path.join(path, data['video'])
        extension = os.path.splitext(file_name)[1][1:]
        codecs = {'mp4': 'mp4v', 'm4v': 'h263', 'avi': 'mp4v'}
        offset = "--start-time " + data['offset'] if 'offset' in data else ''
        quality = data['quality'] if 'quality' in data else None
        vcodec = codecs[extension] if extension in codecs else 'mp4v'
        port = data['port']
        mux = 'ts'
        ip = socket.gethostbyname_ex(socket.gethostname())[2][0]
        
        transcode = 'transcode{vb=%s}' % (quality)
        standard = 'standard{mux=%s,dst=%s:%s,access=http}' % (mux, ip, port)
        sout = standard
        if quality:
            sout = transcode + ':' + standard
        return ['-vvv', '%s' % file_name, '-I', 'dummy', '--sout', '#' + sout]

class VLCThread(threading.Thread):
    processes = {}
    def __init__(self, dir, client, form):
        super(VLCThread, self).__init__()
        self.client = client
        self.dir = dir
        self.form = form
        if self.client in self.processes:
            vlc = self.processes[self.client]
            vlc.terminate()
            vlc.kill()
            VLCProcess.FreePort()
        self.port_num = VLCProcess.AllocatePort().num
        self.form['port'] = self.port_num
        
    def GetPort(self):
        return self.port_num
        
    def run(self):
        print 'Streaming %s to %s on port %s' % (self.form['video'], self.client, self.form['port'])
        vlc = VLCProcess.Make(self.dir, self.form)
        self.processes[self.client] = vlc

 
class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    dir = '..'
    
    @staticmethod
    def SetDir(dir):
        Handler.dir = dir
    
    def do_GET(self):
        client_host, client_port = self.client_address
        print 'Serving %s to %s:%s' % (self.path, client_host, client_port)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        movie_files = ['avi', 'm4v', 'mpg', 'wmv', 'mp4', 'mov', 'mkv', 'flv', 'rm', 'dv']
        audio_files = ['mp3', 'wav']
        nocrawl = open('src/.quickserve_ignore')
        omitRE = nocrawl.read().strip()
        t = template.Template(open('src/server.html.tmpl', 'r').read())
        c = template.Context({
            'Movies': filter(lambda x: os.path.splitext(x)[1][1:] in movie_files and
                             not re.search(omitRE, x), os.listdir(self.dir)),
            'Music': filter(lambda x: os.path.splitext(x)[1][1:] in audio_files and
                            not re.search(omitRE, x), os.listdir(self.dir))
        })
        self.wfile.write(t.render(c))
        
    def do_POST(self):
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
                                environ={'REQUEST_METHOD':'POST',
                                         'CONTENT_TYPE':self.headers['Content-Type']
                                         })
        data = dict(map(lambda x: (str(x), form[x].value), form.keys()))
        print data

        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        th = VLCThread(self.dir, self.client_address, data)
        self.wfile.write(th.GetPort())
        th.start()
        self.wfile.flush()


def main(args):
    port = args.port
    Handler.SetDir(args.dir)
    server = BaseHTTPServer.HTTPServer(("", port), Handler)
    print 'Serving media on port %s' % port
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print ' shutting down'


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-p', '--port', help='The port to host the landing page on.',
                      type='int', default=8888)
    parser.add_option('-d', '--dir', help='The root dir for media.', default='..')
    parser.add_option('-z', '--daemon', help='Whether to run the server as a daemon.',
                      action='store_true')
    options, args = parser.parse_args()
    if options.daemon:
        output = open(tempfile.mkstemp()[0], "w+")
        error = open(tempfile.mkstemp()[0], "w+")

        with daemon.DaemonContext(working_directory=os.getcwd(),
                                  stdout=output, stderr=error):
            main(options);
    else:
        main(options)
        
