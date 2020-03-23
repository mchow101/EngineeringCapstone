from __future__ import print_function
import time
from dual_mc33926_rpi import motors, MAX_SPEED

# Set up sequences of motor speeds.
test_forward_speeds = list(range(0, MAX_SPEED, 1)) + \
  [MAX_SPEED] * 200 + list(range(MAX_SPEED, 0, -1)) + [0]  

test_reverse_speeds = list(range(0, -MAX_SPEED, -1)) + \
  [-MAX_SPEED] * 200 + list(range(-MAX_SPEED, 0, 1)) + [0]  

try:
    motors.enable()
    motors.setSpeeds(0, 0)

    print("Forward")
    for s in test_forward_speeds:
        motors.motor1.setSpeed(s)
        motors.motor2.setSpeed(-s)
        time.sleep(0.005)

    print("Reverse")
    for s in test_reverse_speeds:
        motors.motor1.setSpeed(s)
        motors.motor2.setSpeed(-s)
        time.sleep(0.005)

finally:
  # Stop the motors, even if there is an exception
  # or the user presses Ctrl+C to kill the process.
  motors.setSpeeds(0, 0)
  motors.disable()

