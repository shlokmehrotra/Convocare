import RPi.GPIO as GPIO
import time
import sys
import paho.mqtt.client as mqtt
import ssl
import logging
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

DELAY_BETWEEN_PUBLISH = 120

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    global connected
    print("Connected with result code "+str(rc))
    connected = True

def on_disconnect(client, userdata, flags, rc):
    print("Disconnected with result code "+str(rc))

logging.basicConfig()
client = mqtt.Client()
#allow time to connect to io.adafruit
time.sleep(5)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.enable_logger()
client.username_pw_set(username="vishakh_arora29", password="ffa063303c8d4dcdae4ffc002e22c583")
client.tls_set_context()
#client.tls_set("/etc/ssl/certs/ca-certificates.crt")
#, tls_version=ssl.PROTOCOL_TLSv1_2)
try:
    print("Connecting")
    client.connect("io.adafruit.com", port=8883)
except Exception as err:
    print("Could not connect" + str(err))
    exit(2)
#print("Starting loop")
client.loop_start()

while True:
    if (connected and (GPIO.input(26) == GPIO.HIGH)):
      print("Button pressed")
      time.sleep(1)
      fname = "home/pi/bp.img"
      os.system("fswebcam "+fname)
      time.sleep(1)
      try:
          bp_val = os.system("python imageclassify.py -i "+fname)
      except Exception as e:
          bp_val = 116
      try:
#          print("Publishing heart rate " + heart_rate)
#        client.publish( 'vishakh_arora29/feeds/heart-rate',  payload=heart_rate)
#        time.sleep(DELAY_BETWEEN_PUBLISH)
          print("Publishing blood pressure " + blood_pres)
          client.publish('vishakh_arora29/feeds/blood-pressure', payload=bp_val)
          time.sleep(DELAY_BETWEEN_PUBLISH)
      except Exception as e:
          print("Error publishing:" + str(e))
#      else:
#        print("Not yet connected")
