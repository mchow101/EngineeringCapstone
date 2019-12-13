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

FORWARD_SPEED = MAX_SPEED * 3 / 4
REVERSE_SPEED = MAX_SPEED * 3 / 4
ACCELERATE = list(range(100, FORWARD_SPEED, 10)) + [FORWARD_SPEED]
ACC = True
DEC = False
DEC_VALUE = -18
DECELERATE = list(range(FORWARD_SPEED, 0, DEC_VALUE)) + [0] 
index = 0

MIN_DIST = 60
WINDOW_LENGTH = 5

if __name__ == '__main__':
    try:
	print ("Starting")
        motors.enable()
        motors.setSpeeds(0, 0)
	speed = 0
	lst = [MIN_DIST] * WINDOW_LENGTH
	running_average.average_init(lst)
	init(trig1, echo1)
	init(trig2, echo2)
	init(trig3, echo3)
        while True:
#	    dist = ultrasonic_distance.distance()
            dist = running_average.update(ultrasonic_distance.distance(trig1, echo1))
            #stop if too close
            if dist < MIN_DIST and DEC == False:
                DEC = True
		DECELERATE = list(range(speed, 0, DEC_VALUE)) + [0]
                ACC = False
                index = 0
	    # start if in range
	    elif dist >= MIN_DIST and ACC == False:
		ACC = True
		index = 0
            # reached max speed
            elif ACC == True and speed == FORWARD_SPEED:
                ACC = False
                speed = FORWARD_SPEED
                index = 0
            # stopped
            elif DEC == True and speed == 0:
                DEC = False
                speed = 0
                index = 0
            # accelerate
            elif ACC == True:
                speed = ACCELERATE[index]
                index = index + 1 
            # decelerate
            elif DEC == True:
                speed = DECELERATE[index]
                index = index + 1
            # cruise
	    elif DEC == False and ACC == False and speed > 0:
		speed = FORWARD_SPEED
		index = 0
            else:
                speed = 0
                index = 0
                
            # set speed
            motors.setSpeeds(-speed, speed)
                
            print ("Measured Distance = %.1f cm, Current Speed = %.2f" % (dist, speed))
            time.sleep(.05)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Program stopped by User")
        motors.setSpeeds(0, 0)
        motors.disable()
        GPIO.cleanup()
        
motors.setSpeeds(0, 0)
motors.disable()
