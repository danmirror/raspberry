##---------------------------------##
#	author = Danu andrean
#	create = mey 2019
#-----------------------------------##
#
#


import RPi.GPIO as GPIO 
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14, GPIO.IN, GPIO.PUD_UP)

name = "danu"
print("Hello " + name)

while True:
    if GPIO.input(14) == True:
       print("Door is open")
       time.sleep(2)
    if GPIO.input(14) == False:
       print("Door is closed")
       time.sleep(2)