from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import cv2

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

current_data = {
    'ultra_sonic_distance': None,
    'camera_feed': None,
    'accident_probability': None,
    'system_status': None
}

# 视频流生成器
def generate_camera_feed():
    camera = cv2.VideoCapture(0)  # 使用第一个摄像头
    if not camera.isOpened():
        print("Error: Could not open video device.")
        return
    while True:
        success, frame = camera.read()
        if not success:
            print("Error: Could not read frame.")
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/api/ultra_sonic_distance', methods=['POST'])
def update_distance():
    data = request.json
    current_data['ultra_sonic_distance'] = data.get('ultra_sonic_distance')
    return jsonify({'message': 'Distance updated', 'current_data': current_data})

@app.route('/api/camera_feed')
def camera_feed():
    return Response(generate_camera_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/accident_probability', methods=['POST'])
def update_accident_probability():
    data = request.json
    current_data['accident_probability'] = data.get('accident_probability')
    return jsonify({'message': 'Accident probability updated', 'current_data': current_data})

@app.route('/api/system_status', methods=['POST'])
def update_system_status():
    data = request.json
    current_data['system_status'] = data.get('system_status')
    return jsonify({'message': 'System status updated', 'current_data': current_data})

@app.route('/api/lock', methods=['POST'])
def lock_car():
    # 执行上锁操作
    return jsonify({'message': 'Car locked'})

@app.route('/api/unlock', methods=['POST'])
def unlock_car():
    # 执行解锁操作
    return jsonify({'message': 'Car unlocked'})

@app.route('/api/current_data', methods=['GET'])
def get_current_data():
    return jsonify(current_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
