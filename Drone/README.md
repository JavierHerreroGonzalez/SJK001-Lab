# Autonomous Drone Challenge
## Overview

This folder contains the implementation of an autonomous drone controller for the Drone Rescue People exercise in the Unibotics Robotics Academy.

The goal is to locate survivors in a specified area, using computer vision to detect faces, and then safely return to the starting position. The drone uses a combination of targeted movement and spiral search patterns to maximize the chance of finding all survivors.

## Controller

The drone’s behavior is divided into several phases:

1. Takeoff and move to search area:
The drone first takes off to a set altitude and moves towards the predefined coordinates of the survivor area. Altitude is regulated with proportional control to maintain stability and speed is scaled based on the distance to the target:

- Fast Speed: When far from target
- Slow Speed: When approaching target

2. Fine approach:
Once near the target area, the drone slowly moves to the exact coordinates for precision positioning. This ensures that the subsequent spiral search is centered correctly.

3. Survivor detection:
Faces are detected using OpenCV’s Haar cascade classifier applied to the ventral camera feed. To improve detection across orientations, images are rotated at multiple angles before performing detection. A detected face is only recorded if it is sufficiently far from previously detected survivors, avoiding duplicates.

4. Spiral search:
The drone performs an Archimedean spiral search around the initial target coordinates. This systematic pattern ensures thorough coverage of the search area:

```
r = spiral_a + spiral_b * theta
tx = target_x + r * cos(theta)
ty = target_y + r * sin(theta)
```

- `theta` increments in small steps (`theta_step`)
- `r` grows until the maximum search radius (`max_spiral_radius`)
- The drone moves to each point in the spiral, scanning for faces

5. Return to base:
After completing the search, the drone returns to the starting position (the “boat”) using the same distance-based velocity control and fine approach for precision landing.

6. Mission output:
The program prints the positions of detected survivors and a message indicating the successful completion of the mission.

## Parameters
Since the code is extensive and accomplishes multiple tasks, it makes use of a whole array of different parameters:

- Drone flight
  - `altitude`: The target altitude (in meters) the drone maintains during flight. Ensures the drone is high enough to safely navigate and detect survivors.
  - `approach_tolerance`: Distance (in meters) used to consider that the drone has reached a target position. Helps determine when to stop moving toward a point.
  - `distance_threshold`: Distance (in meters) beyond which the drone moves at `fast_speed`. Used to scale speed depending on proximity to target.
  - `fast_speed`: Velocity (in m/s) applied when the drone is far from a target location. Optimizes travel time.
  - `slow_speed`: Velocity (in m/s) applied when the drone is near the target. Improves precision for delicate maneuvers.

- Spiral search
  - `max_spiral_radius`: Maximum radius (in meters) of the spiral search around the target coordinates. Limits the search area.
  - ``
-
-

## Observations
- Face detection: Rotating the image at multiple angles significantly increases detection success, especially since some survivors are not aligned with the camera.
- Spiral search: The Archimedean spiral pattern efficiently covers the area around the initial target. A smaller `theta_step` gives finer coverage but takes longer.
- Speed control: Scaling velocity based on distance ensures both efficiency (fast travel) and precision (slow near targets).
- Avoiding duplicates: The `is_new_survivor` function prevents multiple detections of the same person.

## Images
The following are some images that give a better understanding of the exercise and the execution process.

- Terminal output:
This is the complete output in the terminal after the drone has succeed in its mission.
<img width="1111" height="425" alt="Captura desde 2025-12-09 19-22-17" src="https://github.com/user-attachments/assets/c65d7e4c-cc35-4b36-bc01-bfa43257cc38" />

- Base:
This is the base, a boat where the drone takes off and where it returns after completing its mission.
<img width="1111" height="397" alt="Captura desde 2025-12-09 19-22-49" src="https://github.com/user-attachments/assets/a91e27e2-6722-4859-a26a-8eab767c31bc" />

- Survivors:
These are the survivors whose faces the drone above them has to recognise.
<img width="1111" height="875" alt="Captura desde 2025-12-09 19-24-41" src="https://github.com/user-attachments/assets/52390d13-ebde-475b-9573-2e1980d60f11" />
