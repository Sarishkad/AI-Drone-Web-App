# Drone Detection Dashboard – Setup Guide

This project is a live drone surveillance dashboard using:
- YOLOv8 for object detection (e.g., potholes or garbage)
- Flask for backend API and streaming
- Google Maps for GPS visualization
- DroneKit to connect to a MAVLink-compatible drone (via telemetry or USB)
- RTSP/USB camera feed for live video

---

## 🚀 Features
- Real-time drone video stream with detections
- Live telemetry display (battery, mode, GPS, etc.)
- Drone control (Arm, Disarm, Land, RTL)
- Detection log with GPS coordinates
- Google Maps integration with drone path + detection markers

---

## 🧩 Requirements

### Hardware
- MAVLink-compatible drone (ArduPilot or PX4)
- Telemetry radio or USB connection to drone (e.g., via COM port)
- RTSP or USB camera connected to drone or PC

### Software Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install required packages
pip install -r requirements.txt
