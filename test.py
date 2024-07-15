import threading
import time
import cv2
from picamera2 import Picamera2, Preview
from yolov5 import YOLOv5

# 初始化 Picamera2
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
picam2.start()

# 加载预训练的YOLOv5模型
model = YOLOv5("/home/pi/DL-PART/DLP/yolov5s.pt")  # 选择模型

# 设置运行持续时间（秒）
run_duration = 100  # 设置为10秒后自动结束

def auto_stop():
    time.sleep(run_duration)
    print(f"自动结束，运行时间达到 {run_duration} 秒。")
    picam2.stop()
    quit()

# 启动自动结束线程
auto_stop_thread = threading.Thread(target=auto_stop)
auto_stop_thread.start()

try:
    while True:
        frame = picam2.capture_array()  # 从相机捕获帧

        # 进行物体检测
        results = model.predict(frame)

        # 处理检测结果
        for *xyxy, conf, cls in results.xyxy[0]:
            label = f'{model.model.names[int(cls)]} {conf:.2f}'
            print(f"检测到物体: {label}")
            cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (0, 0, 255), 2)
            cv2.putText(frame, label, (int(xyxy[0]), int(xyxy[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

        # 显示带检测结果的帧
        cv2.imshow("YOLOv5 Object Detection", frame)


except KeyboardInterrupt:
    print("停止运行...")

# 等待自动结束线程完成
auto_stop_thread.join()

picam2.stop()
cv2.destroyAllWindows()
