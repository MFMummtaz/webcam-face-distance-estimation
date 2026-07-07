# webcam-face-distance-estimation using OpenCV

An interactive Python application that estimates the real-time distance between a user's face and their webcam using a single lens. This project utilizes **OpenCV** and the **Triangle Similarity Theorem** for depth estimation without requiring depth sensors.

---

## How It Works

Because a standard webcam doesn't provide depth data, this project uses a geometric hack called **Triangle Similarity**. 

1. **Interactive Live Calibration:** Lock in your camera's focal length on the fly by pressing a single key.
2. **Robust Logic Guardrails:** Prevents division-by-zero crashes or false readings when a target isn't actively detected in the frame.
3. **Real-Time Tracking:** Using the calculated focal length, the script processes real-time video frames, detects faces via a Haar Cascade classifier, and maps changes in pixel width to estimate distance changes.
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
