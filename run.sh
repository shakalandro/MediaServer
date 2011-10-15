#!/bin/bash

show=

while getopts "sk" flag
do
    case $flag in
    	s)
	    echo "Running in foreground"
	    show="t"
	    ;;
	k)
	    echo "KILLING"
	    kill $(ps aux | grep '[d]aemonStart.py' | awk '{print $2}')
	    exit
	    ;;
	?)
	    echo "UNKNOWN"
	    exit
	    ;;
    esac
done

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
if [ "$show" = "t" ] ; then
	python src/server.py
else
	python src/daemonStart.py &
fi
exit
