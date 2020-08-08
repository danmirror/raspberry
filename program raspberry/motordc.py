##---------------------------------##
#	author = Danu andrean
#	create = mey 2019
#-----------------------------------##
#
#

import sys
import time
import RPi.GPIO as GPIO

StepPinForward=36
StepPinBackward=37
sleeptime=1

GPIO.setmode(GPIO.BOARD)
GPIO.setup(StepPinForward, GPIO.OUT)
GPIO.setup(StepPinBackward, GPIO.OUT)

def forward(x):
    GPIO.output(StepPinForward, GPIO.HIGH)
    print "forwarding running  motor "
    time.sleep(x)
    GPIO.output(StepPinForward, GPIO.LOW)

def reverse(x):
    GPIO.output(StepPinBackward, GPIO.HIGH)
    print "backwarding running motor"
    time.sleep(x)
    GPIO.output(StepPinBackward, GPIO.LOW)

def stop(x):
    GPIO.output(StepPinBackward, GPIO.LOW)
    print "stop motor"
    time.sleep(x)
    GPIO.output(StepPinBackward, GPIO.LOW)


try:
	while True:
		forward(10)
		stop(3)
		reverse(2)
		stop(3)

		
except KeyboardInterrupt:
	GPIO.cleanup()