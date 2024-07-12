from flask import Flask, Response, request, jsonify # type: ignore
from flask_cors import CORS # type: ignore
# from picamera2 import Picamera2 # type: ignore
import time
import cv2

app = Flask(__name__)
app.config['DEBUG'] = True
CORS(app)

# Global variables to store the current values
current_data = {
    'ultra_sonic_distance': None,
    'camera_feed': None,
    'obstacle_speed': None,
    'system_status': None
}

@app.route('/api/ultra_sonic_distance', methods=['POST'])
def update_distance():
    data = request.json
    current_data['ultra_sonic_distance'] = data.get('ultra_sonic_distance')
    return jsonify({'message': 'Distance updated', 'current_data': current_data})

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

def gen():
    try:
        picam2 = Picamera2()
        picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
        picam2.start()
        app.logger.info("Camera started successfully.")
        time.sleep(2)  # Allow the camera to warm up

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
    except Exception as e:
        app.logger.error(f"Error occurred: {e}")

@app.route('/api/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/obstacle_speed', methods=['POST'])
def update_obstacle_speed():
    data = request.json
    current_data['obstacle_speed'] = data.get('obstacle_speed')
    return jsonify({'message': 'Accident probability updated', 'current_data': current_data})

@app.route('/api/system_status', methods=['POST'])
def update_system_status():
    data = request.json
    current_data['system_status'] = data.get('system_status')
    return jsonify({'message': 'System status updated', 'current_data': current_data})

@app.route('/api/lock', methods=['POST'])
def lock_car():
    return jsonify({'message': 'Car locked'})

@app.route('/api/unlock', methods=['POST'])
def unlock_car():
    return jsonify({'message': 'Car unlocked'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
