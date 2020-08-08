#--------------------------
#   autor = Danu andrean
#   date  = mey,2019
#   title = main
#----------------------------------
#   object tracking
#   motor
#   buzezer
#-----------------------------------






import cv2
import numpy as np
import sys
import time
import RPi.GPIO as GPIO

StepPinForward=36
StepPinBackward=37
buzzer = 8


GPIO.setmode(GPIO.BOARD)
GPIO.setup(StepPinForward, GPIO.OUT)
GPIO.setup(StepPinBackward, GPIO.OUT)

GPIO.setup(buzzer,GPIO.OUT)

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


def callback(x):
	pass

cap = cv2.VideoCapture(0)
cv2.namedWindow('image')

ilowH = 0
ihighH = 72

ilowS = 70
ihighS = 205
ilowV = 55
ihighV =255

frame_w = 440
frame_h = 85

min_obj = 10*300
max_obj = frame_w*frame_h/1.5

objectFound = 0
count = 0




# create trackbars for color change
cv2.createTrackbar('lowH','image',ilowH,179,callback)
cv2.createTrackbar('highH','image',ihighH,179,callback)

cv2.createTrackbar('lowS','image',ilowS,255,callback)
cv2.createTrackbar('highS','image',ihighS,255,callback)

cv2.createTrackbar('lowV','image',ilowV,255,callback)
cv2.createTrackbar('highV','image',ihighV,255,callback)



kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))
#font=cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX,2,0.5,0,3,1)

try:
	while True:
		ret, frame=cap.read()
		#frame=cv2.resize(frame,(340,220))

		ilowH = cv2.getTrackbarPos('lowH', 'image')
		ihighH = cv2.getTrackbarPos('highH', 'image')
		ilowS = cv2.getTrackbarPos('lowS', 'image')
		ihighS = cv2.getTrackbarPos('highS', 'image')
		ilowV = cv2.getTrackbarPos('lowV', 'image')
		ihighV = cv2.getTrackbarPos('highV', 'image')


		#convert BGR to HSV
		frameHSV= cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
		######----------------------------------------------------##################
		lower_hsv = np.array([ilowH, ilowS, ilowV])
		higher_hsv = np.array([ihighH, ihighS, ihighV])
		# create the Mask
		mask=cv2.inRange(frameHSV,lower_hsv,higher_hsv)
		#morphology
		maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
		maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

		maskFinal=maskClose
		(_, conts, _)=cv2.findContours(maskFinal.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

		    
		for countour in conts:
       			area = cv2.contourArea(countour)
		    
		
			if ((area <max_obj) & (area >min_obj)):			
				objectFound = 1
				count +=1
				print(count)
				cv2.drawContours(frame,conts,-1,(255,0,0),3)
			
				for i in range(len(conts)):
					x,y,w,h=cv2.boundingRect(conts[i])
					cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0), 2)
					cv2.putText(frame,str(area),(x, y - 20), cv2.FONT_HERSHEY_COMPLEX, 1 ,(0,0,255), 2)
					if (count==10):
						cv2.putText(frame,'Object Found',(50,50), cv2.FONT_HERSHEY_COMPLEX, 2 ,(0,255,0), 2)
			
			else:
				for i in range(len(conts)):
					x,y,w,h=cv2.boundingRect(conts[i])
					cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255), 2)
				#	cv2.putText(frame,str(area),(x, y - 20), cv2.FONT_HERSHEY_COMPLEX, 1 ,(0,0,255), 2)
			
				count =0
       
		cv2.imshow("mask",mask)
		cv2.imshow("cam",frame)
		cv2.waitKey(10)
		#print ilowH, ilowS, ilowV,ihighH,ihighS,ihighV

		if (objectFound==True) & (count==10):
			GPIO.output(buzzer,True)
			print("on")
			forward(2)
			
			GPIO.output(buzzer,False)
			print("off")
			stop(2)
			objectFound = 0
			count = 0
			

		if(cv2.waitKey(1) & 0xFF == ord('q')):
			break


	cv2.destroyAllWindows()
	cap.release()


		
except KeyboardInterrupt:
	GPIO.cleanup()


    
    