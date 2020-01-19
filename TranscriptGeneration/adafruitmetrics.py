#!/usr/bin/python
import sys
import paho.mqtt.client as mqtt
import time
import ssl
import logging
import time
# import transcript_create


DELAY_BETWEEN_PUBLISH = 30

#print(transcript_create.main())
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    """
    Asserts connection
    ________________________________
    Args: client, userdata, flags, rc
    Returns: connection state
    """
    global connected
    print("Connected with result code "+str(rc))
    connected = True

def on_disconnect(client, userdata, flags, rc):
    """
    Status while disconnecting
    ________________________________
    Args: client, userdata, flags, rc
    Returns: disconnection state
    """
    print("Disconnected with result code "+str(rc))

def connect():
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

def main(heart_rate, blood_pres):
    while True:
        time.sleep(2)
        if (connected):
            try:
                if (blood_pres == 0):
                    print("Publishing heart rate " + heart_rate)
                    client.publish( 'vishakh_arora29/feeds/heart-rate',  payload=heart_rate)
                    time.sleep(DELAY_BETWEEN_PUBLISH)
                elif (heart_rate == 0):
                    print("Publishing blood pressure " + blood_pres)
                    client.publish('vishakh_arora29/feeds/blood-pressure', payload=blood_pres)
                    time.sleep(DELAY_BETWEEN_PUBLISH)
                break
            except Exception as e:
                print("Error publishing:" + str(e))
        else:
            print("Not yet connected")

if __name__ == "__main__":
    connect()
    main(heart_rate, blood_pres)
