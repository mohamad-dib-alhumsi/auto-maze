import time
from arduino import *
from arduino_alvik import ArduinoAlvik
import klaar as mf
 
alvik = ArduinoAlvik()
 
level = 0
 
def setup():
    alvik.begin()
    delay(1000)
 
def loop():
  global level
  if alvik.get_touch_left():
    level = 1
    alvik.left_led.set_color(1, 0, 0)
    alvik.right_led.set_color(1, 0, 0)
  if alvik.get_touch_up():
    level = 2
    alvik.left_led.set_color(0, 1, 0)
    alvik.right_led.set_color(0, 1, 0)
  if alvik.get_touch_right():
    level = 3
    alvik.left_led.set_color(0, 0, 1)
    alvik.right_led.set_color(0, 0, 1)
  if alvik.get_touch_down():
    alvik.left_led.set_color(0, 1, 1)
    alvik.right_led.set_color(0, 1, 1)
    level = 0
  # Continuously run the selected level
  if level == 1:
    mf.escape_room_level_1(alvik)
  elif level == 2:
    mf.escape_room_level_2(alvik)
  elif level == 3:
    mf.escape_room_level_3(alvik)
 
def cleanup():
    alvik.stop()
 
start(setup, loop, cleanup)