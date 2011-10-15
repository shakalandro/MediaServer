import daemon
import os

from server import main

output = open("tmp.txt", "w+")
error = open("err.txt", "w+")

with daemon.DaemonContext(working_directory=os.getcwd(),
		stdout=output,
		stderr=error):
	main();
