#-*-coding:utf-8-*
import RPi.GPIO as GPIO
import time

pin = 4 
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin,GPIO.OUT)

times=5
while times:
	GPIO.output(pin,True)
	time.sleep(2)
	GPIO.output(pin,False)
	time.sleep(2)
	times=times-1
	print(times)
