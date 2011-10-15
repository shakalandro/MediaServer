'''
Created on Oct 14, 2011

@author: shakalandro
'''

import subprocess
import unittest
import server
import httplib


class ServerTest(unittest.TestCase):
    server_inst = subprocess.Popen('python ../server.py', shell=True)
        
    def __del__(self, *args, **kwargs):
        self.server_inst.terminate()
    
    def testGetIndex(self):
        expected = ['2.avi', 'beamup.avi', 'bg-for zoom title.avi', 'bloodspurt1.avi']
        self.assertEqual(server.get_index('./data'), expected)

    def testConnect(self):
        connection = httplib.HTTPConnection('localhost:8888')
        connection.request('GET', '/')
        self.assertTrue(connection.getresponse().read())

if __name__ == "__main__":
    unittest.main()