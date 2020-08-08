import RPi.GPIO as GPIO
import smbus as smbus
import time

selenoid = 20
pump = 21
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(selenoid, GPIO.OUT)
GPIO.setup(pump, GPIO.OUT)

while True:
   try:
      GPIO.output(pump, GPIO.HIGH)
      print ("pump")
      time.sleep(2)
      GPIO.output(selenoid, GPIO.HIGH)
      print ("selenoid")
      time.sleep(2)
      GPIO.output(pump, GPIO.LOW)
      GPIO.output(selenoid, GPIO.LOW)
      
      print ("Angka yang di masukan harus 1 atau 0")
      time.sleep(2)

   except KeyboardInterrupt:
      GPIO.cleanup()