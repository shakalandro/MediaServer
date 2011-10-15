#!/bin/bash

# Ensure that VLC is installed
if command -v vim > /dev/null ; then
	echo "VLC is installed."
else
	echo "Please install VLC."
	exit
fi

# Ensure that Python is installed
if command -v python > /dev/null ; then
	echo "Python is installed."
	curDir=`pwd`
	export PYTHONPATH=${PYTHONPATH}:${curDir}/Django-1.3.1:${curDir}/python-daemon-1.5.5
else
	echo "Please install Python."
	exit
fi

# Start the streaming server
python src/daemonStart.py &
exit
