from datetime import datetime
import time

hour = datetime.now().strftime('%H')
minute = datetime.now().strftime('%M')
count = 0
while(1):
   count +=1
   if(count==1):
      print("ddd")
   hour = datetime.now().strftime('%H')
   minute = datetime.now().strftime('%M')
   if(hour=="22" and minute=="22" ):
      print("ddd")
   print("jam" +hour)
   print ("menit ->" +minute +"\t jam -> "+hour)
   time.sleep(1)