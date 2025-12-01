import WebGUI
import HAL
import Frequency
import math
import cv2

sur_x = 36
sur_y = -36

max_speed = 5.0
distance_threshold = 10.0
altitude = 4

HAL.takeoff(altitude)

x, y, z = HAL.get_position()
distance = math.sqrt((sur_x - x)**2 + (sur_y - y)**2)

while distance > distance_threshold:
   dx = sur_x - x
   dy = sur_y - y

   direction_length = math.sqrt(dx**2 + dy**2)
   vx = max_speed * (dx / direction_length) 
   vy = max_speed * (dy / direction_length)

   alt_error = altitude - z
   vz = 0.8 * alt_error
   vz = max(min(vz, 1.0), -1.0)

   HAL.set_cmd_vel(vx, vy, vz, 0)

   x, y, z = HAL.get_position()
   distance = math.sqrt((sur_x - x)**2 + (sur_y - y)**2)

   WebGUI.showImage(HAL.get_frontal_image())
   WebGUI.showLeftImage(HAL.get_ventral_image())

while True:
    HAL.set_cmd_pos(sur_x, sur_y, altitude, 0)

    x, y, z = HAL.get_position()
    distance = math.sqrt((sur_x - x)**2 + (sur_y - y)**2)

    WebGUI.showImage(HAL.get_frontal_image())
    WebGUI.showLeftImage(HAL.get_ventral_image())

    if distance < 0.5:
        break

x = sur_x
y = sur_y
step = 2
max_radius = 30

directions = [(step, 0), (0, step), (-step, 0), (0, -step)]

dir_index = 0
radius = step

while radius <= max_radius:

    for _ in range(2):

        dx, dy = directions[dir_index]

        steps = int(radius / step)
        for _ in range(steps):
            x += dx
            y += dy

            HAL.set_cmd_pos(x, y, altitude, 0)

            while True:
                cx, cy, cz = HAL.get_position()
                d = math.sqrt((x - cx)**2 + (y - cy)**2)
                WebGUI.showImage(HAL.get_frontal_image())
                WebGUI.showLeftImage(HAL.get_ventral_image())
                if d < 0.5:
                    break

        dir_index = (dir_index + 1) % 4

    radius += step

