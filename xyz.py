from arduino import *
from arduino_alvik import ArduinoAlvik

alvik = ArduinoAlvik()

TARGET_YAW = 180          
TOLERANCE = 2             
BASE_SPEED = 15           
MULTIPLIER = 0.5          

def setup():
    alvik.begin()
    delay(1000)

def loop():
    roll, pitch, yaw = alvik.get_orientation()
    print("Yaw:", yaw)

    error = yaw - TARGET_YAW

    if error > 180:
        error -= 360
    elif error < -180:
        error += 360

    if abs(error) <= TOLERANCE:
        alvik.set_wheels_speed(0, 0)
    else:
        turn_speed = BASE_SPEED + abs(error) * MULTIPLIER

        if error > 0:
            alvik.set_wheels_speed(turn_speed, -turn_speed)
        else:
            alvik.set_wheels_speed(-turn_speed, turn_speed)

    delay(100)

def cleanup():
    alvik.stop()

start(setup, loop, cleanup)
