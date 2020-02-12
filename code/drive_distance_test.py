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
REVERSE_SPEED = FORWARD_SPEED # MAX_SPEED / 2
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
	Lspeed = 0
	Rspeed = 0
	lst = [MIN_DIST] * WINDOW_LENGTH
	running_average.average_init(lst)
	ultrasonic_distance.init(trig1, echo1)
	ultrasonic_distance.init(trig2, echo2)
	ultrasonic_distance.init(trig3, echo3)
        while True:
#	    dist = ultrasonic_distance.distance(trig1, echo1)
	    time.sleep(.25)
            dist = running_average.update(ultrasonic_distance.distance(trig1, echo1))
	    time.sleep(.25)
	    left = running_average.update(ultrasonic_distance.distance(trig2, echo2))
	    time.sleep(.25)
	    right = running_average.update(ultrasonic_distance.distance(trig3, echo3))
            #stop if too close
            if dist < MIN_DIST and DEC == False:
		print ("TOO CLOSE")
                DEC = True
		DECELERATE = list(range(Lspeed, -REVERSE_SPEED, DEC_VALUE)) + list(range(-REVERSE_SPEED, 0, -DEC_VALUE))
#		L_DECELERATE = list(range(Lspeed, -REVERSE_SPEED, DEC_VALUE)) + list(range(-REVERSE_SPEED, 0, -DEC_VALUE))
#		R_DECELERATE = list(map(lambda x: Rspeed if 
#		R_DECELERATE = list(map(lambda x: 0 if x < 0 else x, L_DECELERATE))
                ACC = False
		print (DECELERATE)
                index = 0
	    # start if in range
	    elif dist >= MIN_DIST and ACC == False:
		ACC = True
		index = 0
            # reached max speed
            elif ACC == True and (Lspeed == FORWARD_SPEED or Rspeed == FORWARD_SPEED):
		print ("CRUISING")
                ACC = False
                Lspeed = FORWARD_SPEED
                Rspeed = FORWARD_SPEED
                index = 0
            # stopped
#            elif DEC == True and (Lspeed == 0 or Rspeed == 0):
#                print ("STOPPED")
#		DEC = False
#                Lspeed = 0
#                Rspeed = 0
#                index = 0
            # accelerate
            elif ACC == True:
		print ("ACCEERLERLER")
                Lspeed = ACCELERATE[index]
                Rspeed = ACCELERATE[index]
                index = index + 1 
            # decelerate
            elif DEC == True:
		print ("DECELERKERLKEJR")
                Lspeed = DECELERATE[index]
                Rspeed = DECELERATE[index]
#		Lspeed = L_DECELERATE[index]
#		Rspeed = R_DECELERATE[index]
                index = index + 1
		if index >= len(DECELERATE) :
		    index = len(DECELERATE) - 1
            # cruise
	    elif DEC == False and ACC == False and Rspeed > 0 or Lspeed > 0:
		print ("ACTUALLY CRUISING")
		Lspeed = FORWARD_SPEED
		Rspeed = FORWARD_SPEED
		index = 0
            else:
		print ("E STOPPED")
                Lspeed = 0
		Rspeed = 0
                index = 0
                
            # set speed
            motors.setSpeeds(-Lspeed, Rspeed)
            print (str(right) + ' ' + str(left))
            print ("Measured Distance = %.1f cm, Current Speed = %.2f, %.2f" % (dist, Lspeed, Rspeed))
#            time.sleep(.05)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Program stopped by User")
        motors.setSpeeds(0, 0)
        motors.disable()
        GPIO.cleanup()
        
motors.setSpeeds(0, 0)
motors.disable()
