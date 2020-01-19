import sys
import paho.mqtt.client as mqtt
import time
import subprocess

# try:
#     import RPi.GPIO as GPIO
# except RuntimeError:
#     print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

TOPIC_PATH="/dvhacks/record/9"
OFF=0
ON=1
CHANNELS = [3,5,7,8,10,11,12,13,15,16,18,19,21,22,23,24,26,29,31,32,33,35,36,37]
DEBUG = False

def dbg(msg):
    global DEBUG
    if DEBUG:
        print(msg)
        sys.stdout.flush()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    dbg("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    dbg("Subscribing to " + TOPIC_PATH)# +"#")
    client.subscribe( TOPIC_PATH) #+"#")

# Function that abstracts on/off condition for GPIO state
# def gpioStateFor(on):
#     if on:
#         return GPIO.HIGH
#     return GPIO.LOW

# The callback for when a PUBLISH message is received from the server.

def record_audio():
    global f_kill
    f_kill = subprocess.Popen(["python","record_audio.py"])

def stop_record_audio():
    f_kill.terminate()

def publish_audio():
    f = open("/home/pi/doctor1.wav","rb")
    audio = f.read()
    f.close()
    audio_actual = bytearray(audio)
    print("publishing audio")
    client.publish('/dvhacks/record/10',audio)


def on_message(client, userdata, msg):
    print("received")
    command = str(msg.payload)
    #print(command)
    if (command == ("b\'start\'")):
        record_audio()
    if (command == ("b\'stop\'")):
        stop_record_audio()
        publish_audio()

if len(sys.argv) > 1 and sys.argv[1] == '-d':
    DEBUG = True
client = mqtt.Client()

print("connecting")
client.connect("mqtt.eclipse.org")
print("connected")
client.on_connect = on_connect
client.on_message = on_message
# GPIO.setmode(GPIO.BOARD)
# GPIO.setwarnings(False)
# GPIO.setup(CHANNELS, GPIO.OUT)
# GPIO.output(CHANNELS, gpioStateFor(OFF))
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
