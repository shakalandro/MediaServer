import daemon
import os
import server
import tempfile


output = open(tempfile.mkstemp()[0], "w+")
error = open(tempfile.mkstemp()[0], "w+")

with daemon.DaemonContext(working_directory=os.getcwd(),
		stdout=output, stderr=error):
	server.main();
