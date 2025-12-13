import WebGUI
import HAL
import math
import cv2

altitude = 4
survivor_x = 36
survivor_y = -36

approach_tolerance = 0.8
distance_threshold = 10
fast_speed = 6.2
slow_speed = 1.0

max_spiral_radius = 12.5
theta_limit = 22 * math.pi
spiral_a = 1.0
spiral_b = 0.35
theta_step = 0.2
spiral_tolerance = 0.5


survivors_detected = []
face_cascade = cv2.CascadeClassifier(
    "/resources/exercises/rescue_people/haarcascade_frontalface_default.xml"
)

# Take off
HAL.takeoff(altitude)

# Move to the survivors' region
print('Moving to the survivors\' region...')
while True:
   x, y, z = HAL.get_position()
   dx = survivor_x - x
   dy = survivor_y - y
   distance = math.sqrt(dx**2 + dy**2)

   # Check if the drone is very near to the coordinates
   if distance < approach_tolerance:
      break

   # Scale the speed depending on the distance
   speed = fast_speed if distance > distance_threshold else slow_speed
   vx = speed * (dx / distance)
   vy = speed * (dy / distance)

   # Keep altitude stable
   vz = 0.7 * (altitude - z)
   vz = max(min(vz, 1.0), -1.0)
   
   HAL.set_cmd_vel(vx, vy, vz, 0)
   
   WebGUI.showImage(HAL.get_frontal_image())
   WebGUI.showLeftImage(HAL.get_ventral_image())

# Slowly move to the exact coordinates
print('Slowly approaching the position...')
while True:
   x, y, z = HAL.get_position()
   dx = survivor_x - x
   dy = survivor_y - y
   dz = altitude - z
   distance = math.sqrt(dx**2 + dy**2 + dz**2)
   
   HAL.set_cmd_pos(survivor_x, survivor_y, altitude, 0)
   
   WebGUI.showImage(HAL.get_frontal_image())
   WebGUI.showLeftImage(HAL.get_ventral_image())

   # Check if the drone is almost at the coordinates
   if distance < (approach_tolerance / 2):
      break

def detect_face():
    frame = HAL.get_ventral_image()
    gray_original = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Angles to try (covers most ground orientations)
    angles = [0, 45, -45, 90, -90, 135, -135, 180]

    for angle in angles:
        if angle == 0:
            gray = gray_original
        else:
            # Get rotation matrix
            (h, w) = gray_original.shape[:2]
            M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
            gray = cv2.warpAffine(gray_original, M, (w, h))

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        if len(faces) > 0:
            return True

    return False


def is_new_survivor(x, y, survivors, threshold):
    for sx, sy in survivors:
        if math.sqrt((x - sx)**2 + (y - sy)**2) < threshold:
            return False
    return True

# Move in a spiral
theta = 0.0
print('Searching in a spiral...')
r = spiral_a + (spiral_b * theta)
while r <= max_spiral_radius:        
    # Archimedean spiral equation  
    tx = survivor_x + (r * math.cos(theta))
    ty = survivor_y + (r * math.sin(theta))

    # Move to the next spiral point
    while True:
      x, y, z = HAL.get_position()
      d = math.sqrt((tx - x)**2 + (ty - y)**2)
    
      HAL.set_cmd_pos(tx, ty, altitude, 0)
    
      # Detect faces
      if detect_face():
    
        # Avoid duplicate storage
        if is_new_survivor(x, y, survivors_detected, 5.0):
            print(f"Face detected at: ({x:.2f}, {y:.2f})")
            survivors_detected.append((x, y))
    
      WebGUI.showImage(HAL.get_frontal_image())
      WebGUI.showLeftImage(HAL.get_ventral_image())
    
      if d < spiral_tolerance:
         break
      
    theta += theta_step
    r = spiral_a + (spiral_b * theta)

print("Search finished")

# Return to the boat
print("Returning to the boat...")
while True:
   x, y, z = HAL.get_position()
   dx = 0 - x
   dy = 0 - y
   distance = math.sqrt(dx**2 + dy**2)

   # Check if the drone is very near to the coordinates
   if distance < approach_tolerance:
      break

   # Scale the speed depending on the distance
   speed = fast_speed if distance > distance_threshold else slow_speed
   vx = speed * (dx / distance)
   vy = speed * (dy / distance)

   # Keep altitude stable
   vz = 0.7 * (altitude - z)
   vz = max(min(vz, 1.0), -1.0)
   
   HAL.set_cmd_vel(vx, vy, vz, 0)
   
   WebGUI.showImage(HAL.get_frontal_image())
   WebGUI.showLeftImage(HAL.get_ventral_image())

# Slowly move to the exact coordinates
print('Slowly approaching the position...')
while True:
   x, y, z = HAL.get_position()
   dx = 0 - x
   dy = 0 - y
   dz = altitude - z
   distance = math.sqrt(dx**2 + dy**2 + dz**2)
   
   HAL.set_cmd_pos(0, 0, altitude, 0)
   
   WebGUI.showImage(HAL.get_frontal_image())
   WebGUI.showLeftImage(HAL.get_ventral_image())

   # Check if the drone is almost at the coordinates
   if distance < (approach_tolerance / 2):
      break

print("Landing initiated...")
HAL.land()

print("Survivors detected:", survivors_detected)
print("Mission complete")
