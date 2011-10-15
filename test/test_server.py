'''
Created on Oct 14, 2011

@author: shakalandro
'''

import os
import sys
import subprocess
import unittest
import server
import httplib


class ServerTest(unittest.TestCase):
    server_inst = subprocess.Popen('python ../server.py', shell=True)
        
    def __del__(self, *args, **kwargs):
        self.server_inst.terminate()
    
    def testGetIndex(self):
        self.assertTrue(server.get_index('./data', '../src/server.html'))

    def testConnect(self):
        connection = httplib.HTTPConnection('localhost:8888')
        connection.request('GET', '/')
        self.assertTrue(connection.getresponse().read())

if __name__ == "__main__":
    unittest.main()