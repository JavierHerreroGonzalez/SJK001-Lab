import WebGUI
import HAL
import Frequency

import cv2

i = 0
previous_error = 0.0
integral = 0.0
Kp = 0.01
Kd = 0.002
Ki = 0.00001

while True:
    img = HAL.getImage()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    red_mask = cv2.inRange(hsv, (0, 125, 125), (30, 255, 255))
    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    M = cv2.moments(contours[0])

    if M["m00"] != 0:
        cX = M["m10"] / M["m00"]
    else:
        cX = 0

    if cX > 0:

        error = 320 - cX
        derivative = error - previous_error
        integral += error

        w = Kp * error + Kd * derivative + Ki * integral

        if abs(error) > 80:
            HAL.setV(3)
        else:
            HAL.setV(6)

        HAL.setW(w)

        previous_error = error

    WebGUI.showImage(img)

    #print(f'{i} cX: {cX:.2f} error: {error:.2f} w: {w:.2f}')
    i = i + 1
