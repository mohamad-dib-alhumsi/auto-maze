import sys, os
import time

# importeer Alvik library
base_dir = os.path.dirname(os.path.abspath(__file__))  
null_path = os.path.join(base_dir, "null")  
sys.path.append(null_path)  

from arduino_alvik import ArduinoAlvik
from arduino import *

alvik = ArduinoAlvik()

# parameters
distance_cm = 50   # afstand tussen barrières
wheel_diameter_cm = 6.0
wheel_circumference = 3.1416 * wheel_diameter_cm
speed_cm_per_s = 10.0

# bereken tijd
t = distance_cm / speed_cm_per_s

def setup():
    alvik.begin()
    delay(500)

def loop():
    # laat de robot rijden
    alvik.set_wheels_speed(10, 10)  # snelheid (units afhankelijk van library)
    time.sleep(t - 0.3)  # iets minder tijd om botsing te vermijden
    alvik.stop()

def cleanup():
    alvik.stop()

start(setup, loop, cleanup)
