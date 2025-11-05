from arduino import *
import time
 
def escape_room_level_1(alvik):
    # Ruwe afstandsmetingen ophalen
    max_distance = 0
    best_angle = 0
    current_angle = 0
    # Rotation parameters (adjust these based on your robot's calibration)
    ROTATION_SPEED = 10
    SCAN_DURATION = 17500  # Time to complete ~360 degrees (adjust as needed)
    SAMPLE_INTERVAL = 100  # Check distance every 100ms
    # Start rotating
    alvik.set_wheels_speed(-ROTATION_SPEED, ROTATION_SPEED)
    start_time = time.ticks_ms()
    # Scan while rotating
    while time.ticks_ms() - start_time < SCAN_DURATION:
        distances = alvik.get_distance()
        center = distances[2]
        if center > max_distance:
            max_distance == center
            best_angle = time.ticks_ms() - start_time
        delay(SAMPLE_INTERVAL)
    # Stop rotation
    alvik.set_wheels_speed(0, 0)
    delay(500)
    print(f"Max distance: {max_distance} cm at angle {best_angle}ms")
    # Rotate back to the best angle
    alvik.set_wheels_speed(-ROTATION_SPEED, ROTATION_SPEED)
    delay(best_angle)
    alvik.set_wheels_speed(0, 0)
    delay(500)
    # Move forward until obstacle within 5cm
    alvik.set_wheels_speed(30, 30)
    while True:
        distances = alvik.get_distance()
        center = distances[2]
        if center <= 5:
            alvik.set_wheels_speed(0, 0)
            print("Obstacle detected within 5cm!")
            break
        delay(50)
 
was_on_slope = False
 
def escape_room_level_2(alvik):
    global was_on_slope
    BASE_SPEED = 20
    UPHILL_MULTIPLIER = 2.0
    DOWNHILL_MULTIPLIER = 0.5
    PLATEAU_THRESHOLD = 5  # Degrees of pitch to consider "flat"
    STOP_DURATION = 3000  # 3 seconds
    # Track previous state
    prev_pitch = 0
    yaw, pitch, roll = alvik.get_orientation()
    # Determine current terrain
    if pitch < -PLATEAU_THRESHOLD:
        # Uphill
        speed = int(BASE_SPEED * UPHILL_MULTIPLIER)
        alvik.set_wheels_speed(speed, speed)
        was_on_slope = True
        print(f"Uphill: pitch={pitch:.1f}, speed={speed}")
        print(was_on_slope)
    elif pitch > PLATEAU_THRESHOLD:
        # Downhill
        speed = int(BASE_SPEED * DOWNHILL_MULTIPLIER)
        alvik.set_wheels_speed(speed, speed)
        was_on_slope = True
        print(f"Downhill: pitch={pitch:.1f}, speed={speed}")
    else:
        # Plateau detected
        if was_on_slope:
            # Just transitioned to plateau - stop for 3 seconds
            print(f"Plateau detected! pitch={pitch:.1f}, stopping...")
            alvik.set_wheels_speed(0, 0)
            delay(STOP_DURATION)
            was_on_slope = False
        # Continue at base speed
        alvik.set_wheels_speed(BASE_SPEED, BASE_SPEED)
        print(f"Plateau: pitch={pitch:.1f}, speed={BASE_SPEED}")
    prev_pitch = pitch
    delay(100)
 
 
# Global variable for saved colors
saved_colors = []
 
def escape_room_level_3(alvik):
    global saved_colors
    # Parameters
    FORWARD_SPEED = 20
    COLOR_CHANGE_THRESHOLD = 15
    MATCH_TOLERANCE = 10
    OBSTACLE_DISTANCE = 5
    COLOR_CONFIRMATION_COUNT = 3
    # Read distance sensors
    distances = alvik.get_distance()
    center = distances[2]
    # If obstacle within 5cm
    if center < OBSTACLE_DISTANCE:
        alvik.set_wheels_speed(0, 0)
        print("Obstacle detected within 5cm!")
        print(f"Total colors saved: {len(saved_colors)}")
        delay(500)
        return_to_unique_color(alvik, FORWARD_SPEED, MATCH_TOLERANCE)
        return
    # Otherwise, keep moving and scanning colors
    save_color_list_stable(alvik, FORWARD_SPEED, COLOR_CHANGE_THRESHOLD, MATCH_TOLERANCE)
 
 
def save_color_list_stable(alvik, FORWARD_SPEED, COLOR_CHANGE_THRESHOLD, MATCH_TOLERANCE):
    global saved_colors
    COLOR_CONFIRMATION_COUNT = 3
    alvik.set_wheels_speed(FORWARD_SPEED, FORWARD_SPEED)
    stable_reads = []
    # Collect 3 consecutive stable readings
    for _ in range(COLOR_CONFIRMATION_COUNT):
        new_color = alvik.get_color_raw()
        stable_reads.append(new_color)
        delay(50)
    # Check if the 3 readings are close enough
    if all(check_color(stable_reads[0], c, MATCH_TOLERANCE) for c in stable_reads[1:]):
        confirmed_color = average_color(stable_reads)
        # Compare to last saved color
        if saved_colors:
            last_color = saved_colors[-1]
            if not check_color(last_color, confirmed_color, COLOR_CHANGE_THRESHOLD):
                print(f"New color detected! Saving: {confirmed_color}")
                saved_colors.append(confirmed_color)
        else:
            print(f"Saving first color: {confirmed_color}")
            saved_colors.append(confirmed_color)
 
 
def return_to_unique_color(alvik, FORWARD_SPEED, MATCH_TOLERANCE):
    global saved_colors
    if not saved_colors:
        print("No saved colors - nothing to return to.")
        return
    print(f"Analyzing {len(saved_colors)} saved colors...")
    # Count occurrences of each color
    color_counts = {}
    for color in saved_colors:
        found = False
        for ref_color in list(color_counts.keys()):
            if check_color(ref_color, color, MATCH_TOLERANCE):
                color_counts[ref_color] += 1
                found = True
                break
        if not found:
            color_counts[tuple(color)] = 1
    # Find colors that appear only once
    unique_colors = [c for c, count in color_counts.items() if count == 1]
    if not unique_colors:
        print("No unique colors found.")
        return
    target_color = unique_colors[-1]  # Last unique color
    print(f"Returning to unique color: {target_color}")
    # Drive backward until matching that color
    alvik.set_wheels_speed(-FORWARD_SPEED, -FORWARD_SPEED)
    while True:
        current_color = alvik.get_color_raw()
        if check_color(current_color, target_color, MATCH_TOLERANCE):
            print("Reached the unique color!")
            alvik.set_wheels_speed(0, 0)
            DeaD(alvik)
            break
        delay(50)
 
 
# Helper functions
def check_color(c1, c2, tolerance):
    return all(abs(c1[i] - c2[i]) <= tolerance for i in range(3))
 
def average_color(colors):
    r = sum(c[0] for c in colors) // len(colors)
    g = sum(c[1] for c in colors) // len(colors)
    b = sum(c[2] for c in colors) // len(colors)
    return (r, g, b)
 
def DeaD(alvik):
    # Step 1: move forward
    alvik.set_wheels_speed(100, 100)   # both wheels forward
    delay(1000)
    # Step 2: move backward
    alvik.set_wheels_speed(-100, -100)
    delay(1000)
    # Step 3: spin right
    alvik.set_wheels_speed(100, -100)
    delay(1000)
    # Step 4: spin left
    alvik.set_wheels_speed(-100, 100)
    delay(1000)
    # Step 5: wiggle quickly left-right
    for i in range(3):
        alvik.set_wheels_speed(100, -100)
        delay(150)
        alvik.set_wheels_speed(-100, 100)
        delay(150)
    # Stop after the dance
    alvik.stop()
    # Optional: prevent repeating
    while True:
        pass