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
REVERSE_SPEED = FORWARD_SPEED / 2 # MAX_SPEED / 2
# ACCELERATE = list(range(100, FORWARD_SPEED, 10)) + [FORWARD_SPEED]
ACC = True
DEC = False
TURNING = False
STOP = False
ACC_VALUE = 10
STOP_VALUE = 20
Lspeed = 0
Ltarget = 0
Rspeed = 0
Rtarget = 0

MIN_DIST = 60
WINDOW_LENGTH = 5
WALL_DIST = 45

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
            dist = running_average.update(ultrasonic_distance.distance(trig1, echo1))
	        left = running_average.update(ultrasonic_distance.distance(trig2, echo2))
	        right = running_average.update(ultrasonic_distance.distance(trig3, echo3))
            #turn if too close
            if dist < MIN_DIST and TURNING == False:
                print ("TOO CLOSE")
                TURNING = True
            elif TURNING == True and (left <= WALL_DIST or right <= WALL_DIST):
                TURNING = False
                ACC = True
            elif TURNING == True:
                if Rspeed < Lspeed:
                    Rtarget = 0
                    Ltarget = FORWARD_SPEED
                else:
                    Rtarget = FORWARD_SPEED
                    Ltarget = 0
            # start if in range
            elif dist >= MIN_DIST and ACC == False:
                ACC = True
                DEC = False
            # reached max speed
            elif ACC == True and (Lspeed >= FORWARD_SPEED or Rspeed >= FORWARD_SPEED):
                print ("CRUISING FORWARD")
                ACC = False
                Ltarget = FORWARD_SPEED
                Rtarget = FORWARD_SPEED
            # stopping
            elif DEC == True and (Lspeed <= 0 or Rspeed <= 0):
                print ("STOPPING")
                DEC = False
                STOP = True
                Ltarget = 0
                Rtarget = 0
            # stopped
            elif STOP == True and (Lspeed == 0 or Rspeed == 0):
                print ("STOPPED")
                STOP = False
                Ltarget = 0
                Rtarget = 0
            # accelerate
            elif ACC == True:
                print ("ACCEERLERLER")
                Ltarget = FORWARD_SPEED
                Rtarget = FORWARD_SPEED
            # decelerate
            elif DEC == True:
            print ("DECELERKERLKEJR")
                Ltarget = -FORWARD_SPEED
                Rtarget = -FORWARD_SPEED
                # cruise
            elif DEC == False and ACC == False and STOP == False and (Rspeed > 0 or Lspeed > 0):
                print ("ACTUALLY CRUISING")
                Ltarget = FORWARD_SPEED
                Rtarget = FORWARD_SPEED
            else:
                print ("E STOPPED... something's wrong")
                Lspeed = 0
                Rspeed = 0

            #set right speed
            if Rtarget == 0:
                if Rspeed < Rtarget:
                    Rspeed = Rspeed + STOP_VALUE
                elif Rspeed > Rtarget:
                    Rspeed = Rspeed - STOP_VALUE
            elif Rspeed < Rtarget:
                Rspeed = Rspeed + ACC_VALUE
            elif Rspeed > Rtarget:
                Rspeed = Rspeed - ACC_VALUE

            # set left speed
            if Ltarget == 0:
                if Lspeed < Ltarget:
                    Lspeed = Lspeed + STOP_VALUE
                elif Lspeed > Ltarget:
                    Lspeed = Lspeed - STOP_VALUE
            elif Lspeed < Ltarget:
                Lspeed = Lspeed + ACC_VALUE
            elif Lspeed > Ltarget:
                Lspeed = Lspeed - ACC_VALUE

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
