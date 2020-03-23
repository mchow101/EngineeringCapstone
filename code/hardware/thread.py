import threading
import time
from dual_mc33926_rpi import motors, MAX_SPEED
import RPi.GPIO as GPIO
import ultrasonic_distance
import running_average

# constants

trig1 = 17
echo1 = 27
trig2 = 9
echo2 = 11
trig3 = 19
echo3 = 26

def thread_function(name):
    while True:
	print(ultrasonic_distance.distance(trig1, echo1))
	#print(ultrasonic_distance.distance(trig2, echo2))
    	#print(ultrasonic_distance.distance(trig3, echo3))
	print("")
	time.sleep(1)

if __name__ == "__main__":
        try:
	  ultrasonic_distance.init(trig1, echo1)
	  #ultrasonic_distance.init(trig2, echo2)
	  #ultrasonic_distance.init(trig3, echo3)
          print ("Starting")
          motors.enable()
          x = threading.Thread(target=thread_function, args=(1,))
	  x.daemon = True
          x.start()
          while True:
	    motors.setSpeeds(200, 200)
        except KeyboardInterrupt:
                print("Program stopped by User")
                motors.setSpeeds(0, 0)
                motors.disable()
                GPIO.cleanup()
