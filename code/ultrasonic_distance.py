#imports 
import RPi.GPIO as GPIO
import time

#set up GPIO
GPIO.setmode(GPIO.BCM)

def init(GPIO_TRIG, GPIO_ECHO):
        GPIO.setup(GPIO_TRIG, GPIO.OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)

#get distance
def distance(GPIO_TRIG, GPIO_ECHO):
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
        trig1 = 17
        echo1 = 27
        trig2 = 9
        echo2 = 11
	trig3 = 19
	echo3 = 26
	try:
            init(trig1, echo1)
            init(trig2, echo2)
	    init(trig3, echo3)
            dist_sum = 0
            while True:
                dist1 = distance(trig1, echo1)
                dist2 = distance(trig2, echo2)
		dist3 = distance(trig3, echo3)
                time.sleep(1)
                print ("Distance 1 = %.3f cm" % dist1)
                print ("Distance 2 = %.3f cm" % dist2)
		print ("Distance 3 = %.3f cm" % dist3)
		print ("")
        except KeyboardInterrupt:
            print ("Measurement stopped")
            GPIO.cleanup()


