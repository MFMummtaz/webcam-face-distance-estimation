# webcam-face-distance-estimation using OpenCV

An interactive Python application that estimates the real-time distance between a user's face and their webcam using a single lens. This project utilizes **OpenCV** and the **Triangle Similarity Theorem** for depth estimation without requiring depth sensors.

---

## ✨ Features

* **Interactive Live Calibration:** Lock in your camera's focal length on the fly by pressing a single key.
* **Real-time HUD Overlay:** Head-Up Display elements built directly into the video feed to guide the user through setup and active tracking.
* **Robust Logic Guardrails:** Prevents division-by-zero crashes or false readings when a target isn't actively detected in the frame.

---

## How It Works

Because a standard webcam captures 2D images without inherent depth data, this system uses a geometric concept called **Triangle Similarity**. 

1. **The Formula:** The relationship between the camera's focal length ($f$), the actual physical width of the object ($W$), the distance to the object ($D$), and its perceived width in pixels ($P$) is expressed as:
   $$f = \frac{P \times D}{W}$$
2. **Calibration:** By standing at a precisely measured distance (`CALIBRATION_DIST`) and knowing your face's actual width (`TARGET_REAL_WIDTH`), the script locks in your camera's exact focal length ($f$).
3. **Tracking:** Once $f$ is established, the formula is inverted in real-time to solve for the unknown distance ($D$) as your face moves closer or further away:
   $$D = \frac{W \times f}{P}$$
---

## Repository Structure

Ensure your project directory is organized as follows:

```text
webcam-distance-meter/
│
├── haarcascade_frontalface_default.xml   # OpenCV's face detection model
├── distance_estimator.py                # Main application script
├── requirements.txt                     # Project dependencies
└── README.md                            # Project documentation
