#imports 
import RPi.GPIO as GPIO
import time

#set up GPIO
GPIO.setmode(GPIO.BCM)
#GPIO_TRIG = 17
#GPIO_ECHO = 27
GPIO_TRIG = 9
GPIO_ECHO = 11

GPIO.setup(GPIO_TRIG, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

#get distance
def distance():
	#send trigger pulse
	GPIO.output(GPIO_TRIG, True)
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIG, False)

	while GPIO.input(GPIO_ECHO) == 0:
		pass
	start = time.time()

	#wait for return
	while GPIO.input(GPIO_ECHO) == 1:
#		print (GPIO.input(GPIO_ECHO))
		pass
	stop = time.time()

	elapse = stop - start
	distance = (elapse * 34300) / 2

	return distance

if __name__ == '__main__':
	try:
            dist_sum = 0
            while True:
                dist = distance()
                time.sleep(1)
                print ("Distance = %.3f cm" % dist)
        except KeyboardInterrupt:
            print ("Measurement stopped")
            GPIO.cleanup()


