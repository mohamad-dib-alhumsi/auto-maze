from arduino import *
from arduino_alvik import ArduinoAlvik
import time

alvik = ArduinoAlvik()

def setup():
    alvik.begin()
    time.sleep(1)

def loop():
    # 📡 Ruwe afstandsmetingen ophalen
    left, cleft, center, cright, right = alvik.get_distance()

    # 🔄 Afronden op dichtstbijzijnde 5 cm
    sensors = [left, cleft, center, cright, right]
    sensors = [round(val / 5) * 5 for val in sensors]

    # 🚫 Filter: negeer alles ≥ 50 cm
    sensors = [val if val < 50 else 0 for val in sensors]
    left, cleft, center, cright, right = sensors

    print(f"{left} | {cleft} | {center} | {cright} | {right}")
    time.sleep(0.1)

    # 🚨 Check op obstakel binnen 5 cm
    if any(val <= 5 and val > 0 for val in sensors):
        alvik.set_wheels_speed(65, -65)  # Snelle draai
        return

    # 📊 Grootste waarde en verschil bepalen
    max_val = max(sensors)
    others = [v for v in sensors if v != max_val and v > 0]
    min_val = min(others) if others else max_val
    diff = max_val - min_val

    # 🤖 Bewegingslogica
    if max_val == left and diff >= 15:
        alvik.set_wheels_speed(-50, 50)
    elif max_val == cleft and diff >= 15:
        alvik.set_wheels_speed(0, 50)
    elif max_val == center and diff >= 15:
        alvik.set_wheels_speed(40, 40)
    elif max_val == cright and diff >= 15:
        alvik.set_wheels_speed(50, 0)
    elif max_val == right and diff >= 15:
        alvik.set_wheels_speed(50, -50)
    else:
        alvik.set_wheels_speed(30, 30)

def cleanup():
    alvik.stop()

# 🔁 Hoofdlus
try:
    setup()
    while True:
        loop()
except KeyboardInterrupt:
    cleanup()
