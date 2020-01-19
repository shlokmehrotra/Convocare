import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
  if (GPIO.input(26) == GPIO.HIGH):
    print("Button pressed")
    time.sleep(1)
    os.system("fswebcam /home/pi/bp.img")

