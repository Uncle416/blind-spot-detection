from flask import Flask, Response
from picamera2 import Picamera2
import time
import cv2  # OpenCV 用于编码图像

app = Flask(__name__)
app.config['DEBUG'] = True  # 启用调试模式

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
