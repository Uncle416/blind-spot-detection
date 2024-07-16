from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from picamera2 import Picamera2, Preview
import time
import cv2
import json
import os
from threading import Thread
from yolov5 import YOLOv5
import multiprocessing

app = Flask(__name__)
app.config['DEBUG'] = True
CORS(app)
lock = multiprocessing.Lock()

# Global variables to store the current values
ultra_sonic_distance = 0
camera_feed = None
obstacle_type = None
system_status = 0
# Initial system state
car_locked = 1
door_status = 0

# Define the base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Define the paths for the JSON files
distance_file_path = os.path.join(base_dir, '..', 'data', 'distance', 'ultra_sonic_distance.json')
door_file_path = os.path.join(base_dir, '..', 'data', 'door', 'door.json')
status_file_path = os.path.join(base_dir, '..', 'data', 'status', 'system_status.json')

# Function to read ultra_sonic_distance from JSON file periodically
def read_distance_json():
    global ultra_sonic_distance
    while True:
        try:
            with lock:
                with open(distance_file_path, 'r') as f:
                    data = json.load(f)
                    ultra_sonic_distance = data.get('ultra_sonic_distance')
                    calculate_system_status()
        except Exception as e:
            print(f"Error reading distance JSON file: {e}")
        time.sleep(0.005)  # Adjust the interval as needed

# Function to read and write door status from JSON file periodically
def read_write_door_json():
    global car_locked, door_status
    while True:
        try:
            with lock:    
                with open(door_file_path, 'r') as f:
                    data = json.load(f)
                    car_locked = data.get('lock_status')
                    door_status = data.get('door_status')
        except Exception as e:
            print(f"Error reading door JSON file: {e}")
        
        # Write the door status to the JSON file
        try:
            with lock:
                with open(door_file_path, 'w') as f:
                    json.dump({'lock_status': car_locked, 'door_status': door_status}, f)
        except Exception as e:
            print(f"Error writing door JSON file: {e}")
        time.sleep(0.005)  # Adjust the interval as needed

# Function to write system_status to JSON file periodically
def write_status_json():
    global system_status
    while True:
        try:
            with lock:
                with open(status_file_path, 'w') as f:
                    json.dump({'system_status': system_status}, f)
        except Exception as e:
            print(f"Error writing status JSON file: {e}")
        time.sleep(0.005)  # Adjust the interval as needed

# Function to calculate system status
def calculate_system_status():
    global ultra_sonic_distance, obstacle_type, system_status
    if ultra_sonic_distance is None or obstacle_type is None:
        system_status = 0
        return

    if obstacle_type.lower() == 'pedestrian':
        if 0 <= ultra_sonic_distance < 10:
            system_status = 2
        elif 10 <= ultra_sonic_distance < 30:
            system_status = 1
        else:
            system_status = 0
    elif obstacle_type.lower() == 'car':
        if 0 <= ultra_sonic_distance < 20:
            system_status = 2
        elif 20 <= ultra_sonic_distance < 50:
            system_status = 1
        else:
            system_status = 0
    else:
        system_status = 0

# YOLOv5 Initialization
model = YOLOv5("/home/pi/DL-PART/DLP/yolov5s.pt")  # 选择模型

def initialize_camera():
    retries = 5
    for i in range(retries):
        try:
            picam2 = Picamera2()
            picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
            picam2.start()
            app.logger.info("Camera started successfully.")
            return picam2
        except Exception as e:
            app.logger.error(f"Failed to initialize camera (attempt {i+1}/{retries}): {e}")
            time.sleep(2)  # Wait before retrying
    raise RuntimeError("Failed to initialize camera after multiple attempts")

def gen(picam2):
    global obstacle_type
    try:
        while True:
            frame = picam2.capture_array()
            if frame is None:
                app.logger.warning("Captured frame is None.")
                continue

            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                app.logger.warning("Failed to encode frame.")
                continue
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
            
            # Perform object detection
            results = model.predict(frame)
            detected_objects = []
            for *xyxy, conf, cls in results.xyxy[0]:
                label = f'{model.model.names[int(cls)]} {conf:.2f}'
                print(f"检测到物体: {label}")
                detected_objects.append(model.model.names[int(cls)])

            # Update the global obstacle_type with the detected objects
            if detected_objects:
                obstacle_type = detected_objects[0]  # Use the first detected object
            else:
                obstacle_type = "None"

            calculate_system_status()

    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
    finally:
        picam2.stop()
        app.logger.info("Camera stopped successfully.")

@app.route('/api/video_feed')
def video_feed():
    picam2 = initialize_camera()
    return Response(gen(picam2),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/ultra_sonic_distance', methods=['POST'])
def update_distance():
    global ultra_sonic_distance
    data = request.json
    ultra_sonic_distance = data.get('ultra_sonic_distance')
    calculate_system_status()
    return jsonify({'message': 'Distance updated', 'ultra_sonic_distance': ultra_sonic_distance})

@app.route('/api/obstacle_type', methods=['POST'])
def update_obstacle_type():
    global obstacle_type
    data = request.json
    obstacle_type = data.get('obstacle_type')
    calculate_system_status()
    return jsonify({'message': 'Obstacle type updated', 'obstacle_type': obstacle_type})

@app.route('/api/system_status', methods=['POST'])
def update_system_status():
    global system_status
    data = request.json
    system_status = data.get('system_status')
    return jsonify({'message': 'System status updated', 'system_status': system_status})

@app.route('/api/lock', methods=['POST', 'GET'])
def lock_car():
    global car_locked, door_status
    if not car_locked and door_status == 0:
        car_locked = 1
        return jsonify({'message': 'Car locked', 'lock_status': car_locked, 'door_status': door_status})
    return jsonify({'message': 'Cannot lock car', 'lock_status': car_locked, 'door_status': door_status}), 403

@app.route('/api/unlock', methods=['POST', 'GET'])
def unlock_car():
    global car_locked
    car_locked = 0
    return jsonify({'message': 'Car unlocked', 'lock_status': car_locked, 'door_status': door_status})

@app.route('/api/open', methods=['POST', 'GET'])
def open_door():
    global car_locked, door_status
    if car_locked:
        return jsonify({'message': 'Car door cannot be opened as the car is locked'}), 403
    if system_status == 2:
        car_locked = 1
        door_status = 0
        return jsonify({'message': 'Cannot open door due to urgent status. Door locked.', 'lock_status': car_locked, 'door_status': door_status}), 403
    door_status = 1
    return jsonify({'message': 'Car door opened', 'lock_status': car_locked, 'door_status': door_status})

@app.route('/api/close', methods=['POST', 'GET'])
def close_door():
    global car_locked, door_status
    if door_status == 1:
        door_status = 0
        return jsonify({'message': 'Car door closed', 'lock_status': car_locked, 'door_status': door_status})
    return jsonify({'message': 'Door is already closed', 'lock_status': car_locked, 'door_status': door_status})

@app.route('/api/current_data', methods=['GET'])
def get_current_data():
    return jsonify({
        'ultra_sonic_distance': ultra_sonic_distance,
        'obstacle_type': obstacle_type,
        'system_status': system_status,
        'door_status': {
            'lock_status': car_locked,
            'door_status': door_status
        }
    })

if __name__ == '__main__':
    # Start the threads to read JSON files periodically
    Thread(target=read_distance_json).start()
    Thread(target=read_write_door_json).start()
    Thread(target=write_status_json).start()

    app.run(host='0.0.0.0', port=5001, debug=True)
