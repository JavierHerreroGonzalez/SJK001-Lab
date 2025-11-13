# SJK001-Lab - Autonomous Racing Challenge

## Overview

This repository contains the implementations of three controllers for the Visual Follow Line exercise in Unibotics. In this task, a racing car must follow a red line on the track using computer vision and feedback control in order to complete laps efficiently and smoothly.

The controllers implemented here use the detected line position to compute steering commands that minimize the vehicle’s lateral deviation from the racing line.

## Controllers

All controllers share a common processing pipeline:

1. Image Processing:
The car’s camera feed is processed to detect the position of the red line using color filtering and contour analysis.

2. Error Calculation:
The horizontal offset between the line’s centroid (cX) and the center of the image (assumed to be 320 pixels) yields the tracking error:

`error = 320 - cX`

4. Vehicle Control:
The linear velocity is adapted based on how large the error is:

```
if abs(error) > 80:
  HAL.setV(3)
else:
  HAL.setV(6)
```

while the angular velocity is adjusted through a computed variable of the controller logic:

`HAL.setW(w)`

### Proportional Controller

The simplest form of control, where the steering command is proportional to the current error:

```
Kp = 0.01
w = Kp * error
```

Lap time:

<img width="1114" height="300" alt="Captura desde 2025-11-11 17-01-25" src="https://github.com/user-attachments/assets/a8194bdd-6c6c-4a4f-9646-d22f0c3c5038" />

### Proportional Derivative Controller

Adds a derivative term that reacts to changes in the error, providing damping and reducing overshoot:

```
Kp = 0.01
Kd = 0.008
derivative = error - previous_error
w = Kp * error + Kd * derivative
previous_error = error
```

Lap time:

<img width="1114" height="300" alt="Captura desde 2025-11-11 17-03-46" src="https://github.com/user-attachments/assets/d28dc735-c9b3-435a-8a4c-7025b81d6b77" />

### Proportional Integral Derivative Controller

Further introduces an integral term that accumulates past errors to eliminate steady-state offset:

```
Kp = 0.01
Kd = 0.005
Ki = 0.00001
derivative = error - previous_error
integral += error
w = Kp * error + Kd * derivative + Ki * integral
previous_error = error
```

Lap time:

<img width="1114" height="300" alt="Captura desde 2025-11-11 17-08-26" src="https://github.com/user-attachments/assets/f6ef3fd8-1f73-4213-83f9-527d5efaa81a" />

