import os

os.system("arecord -D plughw:1 -f cd -r 16000 -c 1 /home/pi/doctor1.wav")
