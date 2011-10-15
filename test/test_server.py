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
from server import VLCThread


class ServerTest(unittest.TestCase):
    server_inst = subprocess.Popen('python ../server.py', shell=True)
        
    def __del__(self, *args, **kwargs):
        self.server_inst.terminate()
    
    def testGetIndex(self):
        self.assertTrue(server.get_index('./data', '../src/server.html.tmpl'))

    def testConnect(self):
        connection = httplib.HTTPConnection('localhost:8888')
        connection.request('GET', '/')
        self.assertTrue(connection.getresponse().read())
    
    def testMultiUser(self):
        t1 = server.VLCThread(('a', 1), {'video':'The Tourist.mkv'})
        t1.run()
        t2 = server.VLCThread(('a', 1), {'video':'The Tourist.mkv'})
        t2.run()
        self.assertEqual(t1.GetPort(), t2.GetPort())
        
    def testMultiUserClash(self):
        t1 = server.VLCThread(('a', 1), {'video':'The Tourist.mkv'})
        t1.run()
        t2 = server.VLCThread(('a', 2), {'video':'The Tourist.mkv'})
        t2.run()
        self.assertNotEqual(t1.GetPort(), t2.GetPort())

if __name__ == "__main__":
    unittest.main()