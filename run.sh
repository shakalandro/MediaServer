#!/bin/bash

if [ "$1" = "-k" ] ; then 
  echo "Killing the process"
  py=`ps aux | grep '[d]aemonStart.py' | wc -l`
  if [ $py -gt 0 ] ; then
    ps aux | grep '[d]aemonStart.py' | awk '{print $2}' | xargs kill -9
  fi
  vlc=`ps aux | grep '[V]LC' | wc -l`
  if [ $vlc -gt 0 ] ; then
    ps aux | grep '[V]LC' | awk '{print $2}' | xargs kill -9
  fi
  exit
else
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
  python src/server.py $@
fi