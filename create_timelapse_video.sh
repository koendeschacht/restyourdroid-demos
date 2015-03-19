#!/bin/bash

# 
#  Capture images from an android device and create a timelapse video using mencoder.
#  To install mencoder on ubuntu: sudo apt-get install mencoder
#


api_url="http://restyourdroid.com/f/ae4564ss"  # change to the url of your android device


api_request="/camera?binary=true&width=1024"
frame_rate=15

set -e
mkdir timelapse

function ctrl_c() {
  CAPTURE_IMAGES=0
  echo ""
  echo "Creating video"
  mencoder mf://timelapse/*.jpg -mf w=800:h=600:fps=$frame_rate:type=jpg -ovc lavc -lavcopts vcodec=mpeg4:mbd=2:trell -oac copy -o output.avi  > /dev/null
  echo "Finished"
}

trap ctrl_c SIGINT

echo "Capturing images, press ctrl-c to stop capturing images and encode them into a video file";

while true  
  do curl $api_url$api_request > timelapse/img_`date +%s`.jpg -s ; 
  echo "Captured image"
  sleep 1 ; 
done 
