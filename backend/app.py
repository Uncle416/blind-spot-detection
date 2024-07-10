from flask import Flask, Response, request, jsonify # type: ignore
from flask_cors import CORS # type: ignore
import cv2

app = Flask(__name__)
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

# @app.route('/api/camera_feed')
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
    """Video streaming generator function."""
    vs = cv2.VideoCapture(0)
    while True:
        ret,frame=vs.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame=jpeg.tobytes()
        yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
    vs.release()
    cv2.destroyAllWindows() 

@app.route('/api/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')

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
