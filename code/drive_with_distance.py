# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 16:30:17 2019

@author: Mitali
"""

from __future__ import print_function
import time
from dual_mc33926_rpi import motors, MAX_SPEED
import RPi.GPIO as GPIO

FORWARD_SPEED = MAX_SPEED / 2
REVERSE_SPEED = MAX_SPEED / 2
ACCELERATE = list(range(0, FORWARD_SPEED, 1)) + [FORWARD_SPEED]
ACC = True
DEC = False
DECELERATE = list(range(FORWARD_SPEED, 0, -1)) + [0] 
index = 0

MIN_DIST = 15 
 
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 18
GPIO_ECHO = 24
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        motors.enable()
        motors.setSpeeds(0, 0)

        while True:
            dist = distance()
            #stop if too clase
            if dist > MIN_DIST:
                DEC = True
                ACC = False
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
            else:
                speed = 0
                index = 0
                
            # set speed
            motors.setSpeeds(speed, -speed)
                
            print ("Measured Distance = %.1f cm, Current Speed = %.2f" % dist % speed)
            time.sleep(.05)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Program stopped by User")
        motors.setSpeeds(0, 0)
        motors.disable()
        GPIO.cleanup()
        
motors.setSpeeds(0, 0)
motors.disable()