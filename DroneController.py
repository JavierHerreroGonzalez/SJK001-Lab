import WebGUI
import HAL
import math
import cv2

altitude = 4
survivor_x = 36
survivor_y = -36

aproach_tolerance = 0.8
distance_threshold = 10
fast_speed = 5.0
slow_speed = 1.0

theta_limit = 22 * math.pi
spiral_a = 1.0
spiral_b = 0.35
theta_step = 0.12

# Take off
HAL.takeoff(altitude)

# Move to the survivors' region
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

# Move in a spiral
theta = 0.0
while theta < theta_limit:
   # Archimedean spiral equation
   r = spiral_a + (spiral_b * theta)
   tx = survivor_x + (r * math.cos(theta))
   ty = survivor_y + (r * math.sin(theta))

   # Move to the next spiral point
   while True:
      x, y, z = HAL.get_position()
      d = math.sqrt((tx - x)**2 + (ty - y)**2)

      HAL.set_cmd_pos(tx, ty, altitude, 0)

      # Detect faces

      WebGUI.showImage(HAL.get_frontal_image())
      WebGUI.showLeftImage(HAL.get_ventral_image())

      if d < 0.35:
         break
      
   theta += theta_step
