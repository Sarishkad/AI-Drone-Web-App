# 🛸 YOLOv8 Drone Detection Dashboard

This project is a real-time object detection and telemetry dashboard for drones using [YOLOv8](https://github.com/ultralytics/ultralytics), Flask, and DroneKit. It streams live video, detects objects like potholes or garbage, tracks the drone's GPS location, and logs detections on a map with a telemetry panel and control buttons.

---

## 📦 Project Features

- 🎥 **Live RTSP/USB camera stream**
- 🤖 **YOLOv8 real-time detection**
- 📍 **Detection + drone GPS mapping**
- 🗺️ **Google Maps view with detection pins and drone path**
- ⚙️ **Drone telemetry (battery, GPS fix, mode, etc.)**
- 🕹️ **Drone control panel (Arm, Disarm, Land, RTL, Buzzer, Reboot)**

---

## 📁 Repository Structure

├── app.py # Main Flask server
├── templates/
│ └── index.html # Dashboard UI (Google Maps + Detection Log)
├── static/
│ └── assets/... # Icons, styles, etc.
├── setup.md # Environment & dependency setup
├── yolo_model_setup.md # YOLOv8 model setup and testing
├── README.md # Project overview (this file)


---

## 🚀 Getting Started

Follow these steps to get the project running:

1. **Environment Setup**  
   → See [setup.md](./setup.md) for instructions on:
   - Creating a Python virtual environment
   - Installing dependencies (Flask, DroneKit, etc.)
   - Connecting the drone via MAVLink

2. **YOLOv8 Model Setup**  
   → See [yolo_model_setup.md](./yolo_model_setup.md) for:
   - Installing PyTorch and Ultralytics YOLO
   - Testing model predictions
   - Integrating your custom YOLOv8 `.pt` model

3. **Run the App**

```bash
python app.py
