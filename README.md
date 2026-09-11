# Smart Autonomous Drone for Face Tracking and Person Following

This project develops a **smart autonomous tracking system using the DJI Tello drone**. It uses computer vision and **YOLOv3** to detect and track a person, allowing the drone to automatically follow the target.

## Features

- Real-time person detection using YOLOv3
- Face tracking
- Person/body following
- Autonomous drone movement
- Live camera streaming
- Video recording

## How It Works

**DJI Tello Camera → YOLOv3 Detection → Target Tracking → Movement Control → Drone Following**

The DJI Tello camera captures live video. YOLOv3 detects the person and determines the target's position in the camera frame.

A threshold-based control method is used to adjust the drone's movement and keep the target within the desired area of the camera view.

## Technologies

- Python
- OpenCV
- YOLOv3
- Computer Vision
- DJI Tello
- DJITelloPy

## Objective

To develop a vision-based autonomous DJI Tello drone capable of detecting, tracking, and following a person using computer vision.

## Author

**Nur Faizah Hambali**
