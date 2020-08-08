#!/usr/bin/python3

import RPi.GPIO as GPIO
import smbus as smbus
import time 
from datetime import datetime
import requests


class send_web:
    def send(self, selenoid, pump, dist):
        url = "https://api-watercontrol.herokuapp.com/api/v1/data"

        payload = {
        'data1': selenoid,
        'data2': pump,
        'data3': dist
        }

        headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data = payload)

        print(response.text.encode('utf8'))


class relay:
   def __init__(self):
      self.selenoid = 21
      self.pump = 20
      self.lampu_pump = 6
      self.lampu_selenoid = 13
      GPIO.setup(self.selenoid, GPIO.OUT)
      GPIO.setup(self.pump, GPIO.OUT)
      GPIO.setup(self.lampu_pump, GPIO.OUT)
      GPIO.setup(self.lampu_selenoid, GPIO.OUT)
    # off
   def selenoid_high(self):
      GPIO.output(self.selenoid, GPIO.HIGH)
      GPIO.output(self.lampu_selenoid, GPIO.LOW)
      time.sleep(1)
   def pump_high(self):
      GPIO.output(self.pump, GPIO.HIGH)
      GPIO.output(self.lampu_pump, GPIO.LOW)
      time.sleep(1)

    # on
   def selenoid_low(self):
      GPIO.output(self.selenoid, GPIO.LOW)
      GPIO.output(self.lampu_selenoid, GPIO.HIGH)
      time.sleep(1)
   def pump_low(self):
      GPIO.output(self.pump, GPIO.LOW)
      GPIO.output(self.lampu_pump, GPIO.HIGH)
      time.sleep(1)

      
class UltraSonic:
    def __init__(self):
        # GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # set GPIO Pins
        self.GPIO_TRIGGER = 18
        self.GPIO_ECHO = 24

        # set GPIO direction (IN / OUT)
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)

    def distance(self):
        # set Trigger to HIGH
        GPIO.output(self.GPIO_TRIGGER, True)

        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)

        starttime = time.time()
        stoptime = time.time()

        # save StartTime
        while GPIO.input(self.GPIO_ECHO) == 0:
            starttime = time.time()

        # save time of arrival
        while GPIO.input(self.GPIO_ECHO) == 1:
            stoptime = time.time()

        # time difference between start and arrival
        timeelapsed = stoptime - starttime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (timeelapsed * 34300) / 2
        distance = distance*10
        return distance


class I2CLCD:
    def __init__(self):
        # Define some device parameters
        self.I2C_ADDR = 0x27     # I2C device address, if any error, change this address to 0x3f
        self.LCD_WIDTH = 16      # Maximum characters per line

        # Define some device constants
        self.LCD_CHR = 1     # Mode - Sending data
        self.LCD_CMD = 0     # Mode - Sending command

        self.LCD_LINE_1 = 0x80   # LCD RAM address for the 1st line
        self.LCD_LINE_2 = 0xC0   # LCD RAM address for the 2nd line
        self.LCD_LINE_3 = 0x94   # LCD RAM address for the 3rd line
        self.LCD_LINE_4 = 0xD4   # LCD RAM address for the 4th line

        self.LCD_BACKLIGHT = 0x08  # On

        self.ENABLE = 0b00000100     # Enable bit

        # Timing constants
        self.E_PULSE = 0.0005
        self.E_DELAY = 0.0005

        # Open I2C interface
        # bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
        self.bus = smbus.SMBus(1)    # Rev 2 Pi uses 1

        self.lcd_init()

    def lcd_init(self):
        # Initialise display
        self.lcd_byte(0x33, self.LCD_CMD)     # 110011 Initialise
        self.lcd_byte(0x32, self.LCD_CMD)     # 110010 Initialise
        self.lcd_byte(0x06, self.LCD_CMD)     # 000110 Cursor move direction
        self.lcd_byte(0x0C, self.LCD_CMD)     # 001100 Display On,Cursor Off, Blink Off
        self.lcd_byte(0x28, self.LCD_CMD)     # 101000 Data length, number of lines, font size
        self.lcd_byte(0x01, self.LCD_CMD)     # 000001 Clear display
        time.sleep(self.E_DELAY)

    def lcd_byte(self, bits, mode):
        # Send byte to data pins
        # bits = the data
        # mode = 1 for data
        #        0 for command

        bits_high = mode | (bits & 0xF0) | self.LCD_BACKLIGHT
        bits_low = mode | ((bits << 4) & 0xF0) | self.LCD_BACKLIGHT

        # High bits
        self.bus.write_byte(self.I2C_ADDR, bits_high)
        self.lcd_toggle_enable(bits_high)

        # Low bits
        self.bus.write_byte(self.I2C_ADDR, bits_low)
        self.lcd_toggle_enable(bits_low)

    def lcd_toggle_enable(self, bits):
        # Toggle enable
        time.sleep(self.E_DELAY)
        self.bus.write_byte(self.I2C_ADDR, (bits | self.ENABLE))
        time.sleep(self.E_PULSE)
        self.bus.write_byte(self.I2C_ADDR, (bits & ~self.ENABLE))
        time.sleep(self.E_DELAY)

    def lcd_string(self, message, line):
        # Send string to display
        message = message.ljust(self.LCD_WIDTH, " ")

        self.lcd_byte(line, self.LCD_CMD)

        for i in range(self.LCD_WIDTH):
            self.lcd_byte(ord(message[i]), self.LCD_CHR)


if __name__ == '__main__':
    try:
        send = send_web()
        us = UltraSonic()
        lcd = I2CLCD()
        relay = relay()
        isi = False
        selenoid = 0
        pump = 0
        count = 0

        #=======================set val=========================================
        limit_value = 310 #nilai limit nilai ketika tidak ada sensor dalam (mm)

        
        val_selenoid_on = 20 #mm || kurang dari
        val_pump_on = 200 # mm || lebih dari

        #kondisi mati antara up dan down
        val_all_off_up = 160 #mm
        val_all_off_down = 150 #mm
        #----------------------------------------------------------------------------------------


        while True:
            hour = datetime.now().strftime('%H')
            minute = datetime.now().strftime('%M')
            dist = us.distance()
            dist_real = limit_value - dist

		
            if(dist <1000 and minute == "00"): #kurang dari 1m dan minut itu no atau satu jam
                count +=1
                if(count==1):
                    send.send(selenoid,pump, limit_value) #kirim ke website
            else:
                count = 0


            if (hour== "07" ):
                
                
                if (dist_real <= val_all_off_up and dist_real >=val_all_off_down):
                    relay.pump_high()
                    print("kondisi standar batas air")
                    relay.selenoid_high()
                    isi = False
                    selenoid = 0
                    pump = 0
                   
                 
                if(dist_real > val_pump_on):
                    relay.pump_low()
                    relay.selenoid_high()
                    isi = False
                    print("pump on")
                    selenoid = 0
                    pump = 1
                else:
                    relay.pump_high()
                    pump = 0

                if (dist_real < val_selenoid_on ):  #tinggi air kurang dari 20 mm
                    isi = True
                    
                if(isi == True):
                    relay.selenoid_low()
                    selenoid = 1
                    print("selenoid on")
                    
               
                print ("tinggi Air = %.2f mm" % dist_real)
                lcd.lcd_string("tinggi Air:", lcd.LCD_LINE_1)
                lcd.lcd_string(" " + str(format(dist_real, '.2f')) + "mm" +" ->on", lcd.LCD_LINE_2)
                time.sleep(1)
            else:
                relay.pump_high()
                relay.selenoid_high()

                lcd.lcd_string("tinggi Air:", lcd.LCD_LINE_1)
                lcd.lcd_string(" " + str(format(dist_real, '.2f')) + "mm" +" ->off", lcd.LCD_LINE_2)
                print ("waktu aktif pukul 07-08")
                print ("jam -> "+hour+"\t menit -> " +minute)

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()