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
print('Buzzer program')
buzzer = 21
GPIO.setup(buzzer,GPIO.OUT)
delay = 2

try:
	while True:
		GPIO.output(buzzer,True)
		print("on")
		time.sleep(delay)
		GPIO.output(buzzer,False)
		print("off")
		time.sleep(delay)
except KeyboardInterrupt:
	GPIO.cleanup()