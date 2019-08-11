from firebase import firebase
import RPi.GPIO as GPIO
import pygame,sys
import sys
import time
import os
channel=21
channel2 = 20
channel3 = 16
channel4=12
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21,GPIO.IN)
GPIO.setup(20,GPIO.IN) 
GPIO.setup(16,GPIO.IN)
GPIO.setup(12,GPIO.OUT)
#flame
firebase = firebase.FirebaseApplication('https://ornate-ray-233214.firebaseio.com', None)

#######

def h(channel):	
	print("flame detect")
	firebase.patch('/etat',{'flame':"YES"})
	time.sleep(5)
	firebase.patch('/etat',{'flame':"NO"})
	

  
GPIO.add_event_detect(channel, GPIO.FALLING, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, h)  # assign function to GPIO PIN, Run function on change

#winter
def h1(channel2):
	print("Winter detect")
	firebase.patch('/etat',{'winter':"YES"})
	
GPIO.add_event_detect(channel2, GPIO.FALLING, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel2, h1)  # assign function to GPIO PIN, Run function on change

#soiL moisture
def h3(channel3):	
	firebase.patch('/etat',{'soil':"Done"})
	print("Good Crop")

  
GPIO.add_event_detect(channel3, GPIO.FALLING, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel3, h3)  # assign function to GPIO PIN, Run function on change
#########

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

temp_sensor = '/sys/bus/w1/devices/28-000005e91e4f/w1_slave'

def temp_raw():
  f = open(temp_sensor,'r')
  lines = f.readlines()
  f.close()
  return lines

def read_temp():
  lines = temp_raw()
  while lines[0].strip()[-3:] != 'YES':
    time.sleep(0.2)
    lines = temp_raw()
  temp_output = lines[1].find('t=')
  if temp_output != -1:
    temp_string = lines[1][temp_output+2:]
    temp_c = float(temp_string)/1000.0
    return temp_c
while True:
	
	result = firebase.get('/etat','start')
	firebase.patch('/etat',{'temperature':str(read_temp())})
	print result
	if result == "off":
		GPIO.output(12,GPIO.LOW)	 
		 
	else:	
		GPIO.output(12,GPIO.HIGH)
		
		
	firebase.post('data/temperature',str(read_temp()))
	
				 
	
	 
		
		
		
