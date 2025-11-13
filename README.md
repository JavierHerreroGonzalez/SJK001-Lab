# SJK001-Lab - Autonomous Racing Challenge

## Overview

This repository contains the implementations of three controllers for the Visual Follow Line exercise in Unibotics.

In this challenge, a racing car must follow a red line on the track using computer vision and feedback control, adjusting its steering to minimize lateral deviation and complete laps efficiently and smoothly.

The controllers implemented here use the detected line position to compute steering commands that keep the vehicle aligned with the racing line.

## Controllers

All controllers share a common processing pipeline:

1. Image Processing:
The car’s camera feed is converted to HSV and thresholded to detect the red line. Contour extraction is then used to compute the centroid of the line.

2. Error Calculation:
The horizontal offset between the line’s centroid (cX) and the center of the image (assumed to be 320 pixels) defines the tracking error:

`error = 320 - cX`

4. Vehicle Control:
The linear velocity is adjusted based on the magnitude of the error:

```
if abs(error) > 80:
  HAL.setV(3)
else:
  HAL.setV(6)
```

The angular velocity is controlled using variables computed by each controller:

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

Adds a derivative term that reacts to changes in the error, helping reduce overshoot and improving stability:

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

Further introduces an integral term that accumulates past errors to reduce long-term bias:

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

## Observations

- Proportional Controller (P):\
Provides reasonably stable control but reacts slowly when exiting curves.
The absence of a damping term leads to noticeable oscillations and delayed course correction, resulting in the worst lap time among the three controllers.

- Proportional Derivative Controller (PD):\
Offers the best overall stability. The derivative term dampens the response and reduces oscillations, allowing the car to recover from turns more quickly and smoothly.\
This resulted in the fastest lap time.

- Proportional Integral Derivative Controller (PID):\
Performs similarly to the P controller but introduces additional instability. Only a very small integral gain was usable, as higher values caused significant overshoot and oscillatory steering.\
In this particular task, the integral component provides minimal benefit due to the continuously changing nature of the tracking error, leading to a lap time slightly worse than the PD controller.

- Additional Note:\
Debug print statements inside the control loop noticeably degraded performance due to resource usage and timing delays. For this reason, they were commented out during testing.
