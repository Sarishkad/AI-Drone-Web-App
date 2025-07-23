from flask import Flask, render_template, Response, jsonify
import cv2
from ultralytics import YOLO
import threading
import time
import torch
import asyncio
from dronekit import connect, VehicleMode

app = Flask(__name__)

# Load YOLOv8 model
model = YOLO('Pothole-Detection/best.pt')
# model = YOLO('Garbage-Detection/best.pt')

RTSP_STREAM_URL = 0
# RTSP_STREAM_URL = "rtsp://192.168.137.53:554/stream"

print("Using CUDA:", torch.cuda.is_available())

# MAVLink connection
MAVLINK_PORT = "COM5"
MAVLINK_BAUD = 57600

print("Connecting to Drone via MAVLink telemetry...")
vehicle = connect(MAVLINK_PORT, baud=MAVLINK_BAUD, wait_ready=False)
print("Connected to Drone via MAVLink telemetry.")

# Global variables
latest_frame = None
lock = threading.Lock()
last_sent_time = 0
COOLDOWN_SECONDS = 5
detection_log = []

# Pune fallback
DEFAULT_LAT = 18.516726
DEFAULT_LON = 73.856255

# Async setup
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


def run_async_loop():
    asyncio.set_event_loop(loop)
    loop.run_forever()


threading.Thread(target=run_async_loop, daemon=True).start()


# Get current GPS from drone or fallback
def get_drone_gps():
    lat = vehicle.location.global_frame.lat
    lon = vehicle.location.global_frame.lon

    if lat == 0.0 or lon == 0.0:
        return DEFAULT_LAT, DEFAULT_LON
    return lat, lon


# Camera thread
def capture_thread():
    global latest_frame
    cap = cv2.VideoCapture(RTSP_STREAM_URL)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    while True:
        success, frame = cap.read()
        if success:
            with lock:
                latest_frame = frame
        else:
            print("Camera read failed.")
            time.sleep(1)


threading.Thread(target=capture_thread, daemon=True).start()


# Inference thread
def generate_frames():
    global latest_frame, last_sent_time, detection_log

    while True:
        with lock:
            frame = latest_frame.copy() if latest_frame is not None else None

        if frame is None:
            time.sleep(0.1)
            continue

        try:
            results = model(frame, conf=0.5, imgsz=640, verbose=False)
            annotated = results[0].plot()

            if results[0].boxes and len(results[0].boxes) > 0:
                current_time = time.time()
                if current_time - last_sent_time > COOLDOWN_SECONDS:
                    last_sent_time = current_time
                    lat, lon = get_drone_gps()

                    detection_log.append({
                        'id': len(detection_log) + 1,
                        'time': time.strftime("%Y-%m-%d %H:%M:%S"),
                        'latitude': lat,
                        'longitude': lon,
                        'severity': "High"
                    })

            _, buffer = cv2.imencode('.jpg', annotated)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

        except Exception as e:
            print("Inference error:", e)
            time.sleep(0.1)


# Function to activate the buzzer
def ring_buzzer():
    print("Buzzer command received (no action performed).")


def reboot_flight_controller():
    print("Reboot command received (no action performed).")


# Flask Routes
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/log')
def get_log():
    return jsonify(detection_log)


@app.route('/telemetry')
def telemetry():
    gps = vehicle.location.global_frame
    return jsonify({
        'mode': vehicle.mode.name if vehicle.mode else 'N/A',
        'battery': round(vehicle.battery.voltage, 2) if vehicle.battery and vehicle.battery.voltage else 'N/A',
        'gps_fix': gps and gps.lat not in (None, 0.0),
        'latitude': gps.lat if gps and gps.lat else None,
        'longitude': gps.lon if gps and gps.lon else None,
        'satellites': vehicle.gps_0.satellites_visible if vehicle.gps_0 and vehicle.gps_0.satellites_visible else 0,
        'is_armable': vehicle.is_armable if vehicle else False,
        'armed': vehicle.armed if vehicle else False
    })


@app.route("/control/<action>", methods=["POST"])
def control_drone(action):
    if action == "arm":
        vehicle.armed = True
    elif action == "disarm":
        vehicle.armed = False
    elif action == "land":
        vehicle.mode = VehicleMode("LAND")
    elif action == "rtl":
        vehicle.mode = VehicleMode("RTL")
    elif action == "buzzer":
        ring_buzzer()
    elif action == "reboot":
        reboot_flight_controller()
    return jsonify({"status": "success", "action": action})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
