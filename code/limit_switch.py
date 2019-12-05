import RPi.GPIO as GPIO
import time
prev = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.IN)

while True:
	input = (GPIO.input(26))
	print (input)
	if ((not input == prev) and input):
		print ("PRess")
	prev = input
	time.sleep(.05)
