from flask import Flask, Response, request, jsonify # type: ignore
from flask_cors import CORS # type: ignore
from picamera2 import Picamera2, Preview # type: ignore
import time
import cv2
import json
import os
from threading import Thread
from yolov5 import YOLOv5

app = Flask(__name__)
app.config['DEBUG'] = True
CORS(app)

car_locked = False

# Global variables to store the current values
current_data = {
    'ultra_sonic_distance': None,
    'camera_feed': None,
    'obstacle_type': None,
    'system_status': None
}

# Define the base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Define the paths for the JSON files
distance_file_path = os.path.join(base_dir, '..', 'data', 'distance', 'ultra_sonic_distance.json')
obstacle_file_path = os.path.join(base_dir, '..', 'data', 'type', 'obstacle_type.json')

# Function to read ultra_sonic_distance from JSON file periodically
def read_distance_json():
    global current_data
    while True:
        try:
            with open(distance_file_path, 'r') as f:
                data = json.load(f)
                current_data['ultra_sonic_distance'] = data.get('ultra_sonic_distance')
        except Exception as e:
            print(f"Error reading distance JSON file: {e}")
        time.sleep(5)  # Adjust the interval as needed

# Function to read obstacle_type from JSON file periodically
def read_obstacle_json():
    global current_data
    while True:
        try:
            with open(obstacle_file_path, 'r') as f:
                data = json.load(f)
                current_data['obstacle_type'] = data.get('obstacle_type')
        except Exception as e:
            print(f"Error reading obstacle JSON file: {e}")
        time.sleep(5)  # Adjust the interval as needed

# @app.route('/api/video_feed')
# def camera_feed():
#     def generate():
#         while True:
#             cap = cv2.VideoCapture(0)  # Open the default camera
#             if not cap.isOpened():
#                 print("Error: Could not open video device.")
#                 continue

#             while cap.isOpened():
#                 ret, frame = cap.read()
#                 if not ret:
#                     print("Error: Could not read frame.")
#                     break

#                 _, buffer = cv2.imencode('.jpg', frame)
#                 frame = buffer.tobytes()
#                 yield (b'--frame\r\n'
#                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#             cap.release()
#             print("Reconnecting to the camera...")

#     return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

# YOLOv5 and Picamera2 Initialization
picam2 = Picamera2()
camera_config = picam2.create_video_configuration(main={"size": (640, 480)})
picam2.configure(camera_config)
picam2.start()

model = YOLOv5("/home/pi/DL-PART/DLP/yolov5s.pt")  # 选择模型

def gen():
    try:
        while True:
            frame = picam2.capture_array()
            if frame is None:
                app.logger.warning("Captured frame is None.")
                continue

            # Perform object detection
            results = model.predict(frame)
            for *xyxy, conf, cls in results.xyxy[0]:
                label = f'{model.model.names[int(cls)]} {conf:.2f}'
                print(f"检测到物体: {label}")
                cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (0, 0, 255), 2)
                cv2.putText(frame, label, (int(xyxy[0]), int(xyxy[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                app.logger.warning("Failed to encode frame.")
                continue
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
    except Exception as e:
        app.logger.error(f"Error occurred: {e}")

@app.route('/api/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/ultra_sonic_distance', methods=['POST'])
def update_distance():
    data = request.json
    current_data['ultra_sonic_distance'] = data.get('ultra_sonic_distance')
    return jsonify({'message': 'Distance updated', 'current_data': current_data})

@app.route('/api/obstacle_type', methods=['POST'])
def update_obstacle_type():
    data = request.json
    current_data['obstacle_type'] = data.get('obstacle_type')
    return jsonify({'message': 'Accident probability updated', 'current_data': current_data})

@app.route('/api/system_status', methods=['POST'])
def update_system_status():
    data = request.json
    current_data['system_status'] = data.get('system_status')
    return jsonify({'message': 'System status updated', 'current_data': current_data})

@app.route('/api/lock', methods=['POST','GET'])
def lock_car():
    global car_locked
    car_locked = True
    return jsonify({'message': 'Car locked'})

@app.route('/api/unlock', methods=['POST','GET'])
def unlock_car():
    global car_locked
    car_locked = False
    return jsonify({'message': 'Car unlocked'})

@app.route('/api/open', methods=['POST','GET'])
def open_door():
    if car_locked:
        return jsonify({'message': 'Car door cannot be opened as the car is locked'}), 403
    return jsonify({'message': 'Car door opened'})

@app.route('/api/close', methods=['POST','GET'])
def close_door():
    return jsonify({'message': 'Car door closed'})

@app.route('/api/current_data', methods=['GET'])
def get_current_data():
    return jsonify(current_data)

if __name__ == '__main__':
    # Start the threads to read JSON files periodically
    Thread(target=read_distance_json).start()
    Thread(target=read_obstacle_json).start()

    app.run(host='0.0.0.0', port=5001, debug=True)
