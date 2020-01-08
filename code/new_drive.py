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

FORWARD_SPEED = MAX_SPEED * 5 / 8
REVERSE_SPEED = FORWARD_SPEED # MAX_SPEED / 2
# ACCELERATE = list(range(100, FORWARD_SPEED, 10)) + [FORWARD_SPEED]
ACC = True
DEC = False
STOP = False
ACC_VALUE = 10
STOP_VALUE = 20
Lspeed = 0
Rspeed = 0

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
#	ultrasonic_distance.init(trig2, echo2)
#	ultrasonic_distance.init(trig3, echo3)
        while True:
            dist = running_average.update(ultrasonic_distance.distance(trig1, echo1))
#	    left = running_average.update(ultrasonic_distance.distance(trig2, echo2))
#	    right = running_average.update(ultrasonic_distance.distance(trig3, echo3))
            #stop if too close
            if dist < MIN_DIST and DEC == False:
		print ("TOO CLOSE")
                DEC = True
                ACC = False
	    # start if in range
	    elif dist >= MIN_DIST and ACC == False:
		ACC = True
                DEC = False
            # reached max speed
            elif ACC == True and (Lspeed >= FORWARD_SPEED or Rspeed >= FORWARD_SPEED):
		print ("CRUISING FORWARD")
                ACC = False
                Lspeed = FORWARD_SPEED
                Rspeed = FORWARD_SPEED
            elif DEC == True and (Lspeed <= -REVERSE_SPEED or Rspeed <= -REVERSE_SPEED):
		print ("CRUISING REVERSE")
                DEC = False
                Lspeed = -REVERSE_SPEED
                Rspeed = -REVERSE_SPEED
            # stopped
            elif STOP == True and (Lspeed == 0 or Rspeed == 0):
                print ("STOPPED")
		STOP = False
                Lspeed = 0
                Rspeed = 0
            # accelerate
            elif ACC == True:
		print ("ACCEERLERLER")
                Lspeed = Lspeed + ACC_VALUE
                Rspeed = Rspeed + ACC_VALUE
            # decelerate
            elif DEC == True:
		print ("DECELERKERLKEJR")
                Lspeed = Lspeed - ACC_VALUE
                Rspeed = Rspeed - ACC_VALUE
            # cruise
	    elif DEC == False and ACC == False and STOP == False and (Rspeed > 0 or Lspeed > 0):
		print ("ACTUALLY CRUISING")
		Lspeed = FORWARD_SPEED
		Rspeed = FORWARD_SPEED
            else:
		print ("E STOPPED")
                Lspeed = 0
		Rspeed = 0
                
            # set speed
            motors.setSpeeds(-Lspeed, Rspeed)
                
            print ("Measured Distance = %.1f cm, Current Speed = %.2f, %.2f" % (dist, Lspeed, Rspeed))
            time.sleep(.05)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Program stopped by User")
        motors.setSpeeds(0, 0)
        motors.disable()
        GPIO.cleanup()
        
motors.setSpeeds(0, 0)
motors.disable()
