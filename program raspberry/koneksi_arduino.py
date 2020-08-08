import serial
import time

ser = serial.Serial ('/dev/ttyUSB0'  , 9600)
ser.write('0')
baca = ser.read()
while(True):
	print(baca)
	time.sleep(1)