import WebGUI
import HAL
import math
import cv2

altitude = 4
survivor_x = 36
survivor_y = -36
aproach_tolerance = 0.4
distance_threshold = 10
fast_speed = 5.0
slow_speed = 1.0

# Take off
HAL.takeoff(altitude)

# Aproach the survivors' region
while True:
   x, y, z = HAL.get_position()
   dx = survivor_x - x
   dy = survivor_y - y
   distance = math.sqrt(dx**2 + dy**2)

   # Check if the drone is almost at the coordinates
   if distance < approach_tolerance:
      break

   # Set the speed according to the distance to the coordinates
   speed = fast_speed if distance > distance_threshold else slow_speed
   vx = speed * (dx / distance)
   vy = speed * (dy / distance)

   # Set the vertical velocity to avoid descending
   vz = 0.7 * (altitude - z)
   vz = max(min(vz, 1.0), -1.0)
   
   HAL.set_cmd_vel(vx, vy, vz, 0)
   
   WebGUI.showImage(HAL.get_frontal_image())
   WebGUI.showLeftImage(HAL.get_ventral_image())

# Move in a spiral
