import time
import threading
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
REVERSE_SPEED = FORWARD_SPEED * 9 / 10
TURN_SPEED = MAX_SPEED * 4 / 5
ACC_VALUE = 10
STOP_VALUE = 20

ACC = True
DEC = False
TURNING = False
STOP = False

Lspeed = 0
Ltarget = 0
Rspeed = 0
Rtarget = 0
dist = 0
left = 0
right = 0
turn_time = 0

SENSOR_DELAY = 0.1
MIN_DIST = 30
WINDOW_LENGTH = 5
WALL_DIST = MIN_DIST + 5

def ultrasonic1():
    while True:
        global dist
	dist = running_average.update(ultrasonic_distance.distance(trig1, echo1))
	time.sleep(SENSOR_DELAY)

def ultrasonic2():
    while True:
	return 100
#	global left
#	left = running_average.update(ultrasonic_distance.distance(trig2, echo2))
#	time.sleep(SENSOR_DELAY)

def ultrasonic3():
    while True:
	return 100
#	global right
#	right = running_average.update(ultrasonic_distance.distance(trig3, echo3))
#       time.sleep(SENSOR_DELAY)

if __name__ == '__main__':
    try:
        print ("Starting")
        #motor setup
        motors.enable()
        motors.setSpeeds(0, 0)
        Lspeed = 0
        Rspeed = 0
        lst = [MIN_DIST] * WINDOW_LENGTH
        #ultrasonic setup
        running_average.average_init(lst)
        ultrasonic_distance.init(trig1, echo1)
#        ultrasonic_distance.init(trig2, echo2)
#        ultrasonic_distance.init(trig3, echo3)
        x = threading.Thread(target=ultrasonic1, args=())
        x.daemon = True
        x.start()
#	y = threading.Thread(target=ultrasonic2, args=())
#	y.daemon = True
#	y.start()
#	z = threading.Thread(target=ultrasonic3, args=())
#	z.daemon = True
#	z.start()
        while True:
            #turn if too close
            if dist < MIN_DIST and TURNING == False:
                print ("TOO CLOSE")
                TURNING = True
            elif TURNING == True and (dist >= MIN_DIST):
                time.sleep(0.4)
                print ("EXITING TURNING")
		TURNING = False
                ACC = True
            elif TURNING == True:
#		print ("TURNING")
                if Rspeed <= Lspeed:
                    Rtarget = -REVERSE_SPEED
                    Ltarget = TURN_SPEED
                else:
                    Rtarget = TURN_SPEED
                    Ltarget = -REVERSE_SPEED
            # start if in range
            elif dist >= MIN_DIST and ACC == False:
#		print ("ACCELERATING")
                ACC = True
                DEC = False
            # reached max speed
            elif ACC == True and (Lspeed >= FORWARD_SPEED or Rspeed >= FORWARD_SPEED):
#                print ("CRUISING FORWARD")
                ACC = False
                Ltarget = FORWARD_SPEED
                Rtarget = FORWARD_SPEED
            # stopping
            elif DEC == True and (Lspeed <= 0 or Rspeed <= 0):
#                print ("STOPPING")
                DEC = False
                STOP = True
                Ltarget = 0
                Rtarget = 0
            # stopped
            elif STOP == True and (Lspeed == 0 or Rspeed == 0):
#                print ("STOPPED")
                STOP = False
                Ltarget = 0
                Rtarget = 0
            # accelerate
            elif ACC == True:
#                print ("ACCEERLERLER")
                Ltarget = FORWARD_SPEED
                Rtarget = FORWARD_SPEED
            # decelerate
            elif DEC == True:
#                print ("DECELERKERLKEJR")
                Ltarget = -FORWARD_SPEED
                Rtarget = -FORWARD_SPEED
            # cruise
            elif DEC == False and ACC == False and STOP == False and (Rspeed > 0 or Lspeed > 0):
#                print ("ACTUALLY CRUISING")
                Ltarget = FORWARD_SPEED
                Rtarget = FORWARD_SPEED
            else:
#                print ("E STOPPED... something's wrong")
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
#            print ("Measured Distance = %.1f cm, Current Speed = %.2f, %.2f" % (dist, Lspeed, Rspeed))
#            print ("Left = %.1f cm, Right = %.1f cm" % (left, right))
#            #time.sleep(.05)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Program stopped by User")
        motors.setSpeeds(0, 0)
        motors.disable()
        GPIO.cleanup()
        
motors.setSpeeds(0, 0)
motors.disable()
