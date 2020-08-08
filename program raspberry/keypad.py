#author = Danu andrean
#keypad 4*4






import RPi.GPIO as GPIO
import time
import getpass


GPIO.setmode(GPIO.BOARD)
MATRIX = [ [1,2,3,'A'],
           [4,5,6,'B'],
           [7,8,9,'C'],
           ['*',0,'#','D'] ]

ROW = [37,35,33,31]
COL = [29,15,13,11]

pas = [1,2,3]
verify = []


for j in range (4):
       GPIO.setup(COL[j], GPIO.OUT)
       GPIO.output(COL[j], 1)

for i in range (4):
       GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)

try:
      while(True):
              for j in range(4):
                    GPIO.output(COL[j],0)
                    ##codice qua##
                    for i in range(4):
                         if GPIO.input(ROW[i]) == 0:
                               value = MATRIX[i][j]
			       print (value)
			       if(value):
			       	      if(value <= str(len(pas))):
				     		verify.append(value)
				      		print(verify)      
			       if(value=="D"):
			              if(pas==verify):
				      		print("data benar")
						pas_done = True
				      else:
						verify=[]
                               while(GPIO.input(ROW[i]) == 0):
                                      pass
                    GPIO.output(COL[j],1)
	      
              time.sleep(0.01)



except KeyboardInterrupt:
	GPIO.cleanup()




#main
if(value):
	print("ok")