import WebGUI
import HAL
import Frequency
import cv2

i = 0
Kp = 0.01

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
        w = Kp * error
        
        if abs(error) > 80:
            HAL.setV(3)
        else:
            HAL.setV(6)
    
        HAL.setW(w)

    WebGUI.showImage(img)

    #print(f'{i} cX: {cX:.2f} error: {error:.2f} w: {w:.2f}')
    i = i + 1
