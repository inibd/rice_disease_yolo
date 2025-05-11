import cv2
from ultralytics import YOLO
import os

model = None  # 全局加载模型


def load_model(model_path):
    """加载模型（首次调用时自动加载）"""
    global model
    if model is None:
        model = YOLO(model_path)
    return model


def detect_diseases(image_path):
    """执行病害检测"""
    model = load_model("models/best.pt")  # 修改为你的模型路径
    results = model(image_path)

    # 解析结果
    detections = []
    for result in results:
        for box in result.boxes:
            detections.append({
                'class_id': int(box.cls[0]),
                'class_name': result.names[int(box.cls[0])],
                'confidence': float(box.conf[0]),
                'bbox': box.xyxy[0].tolist()  # [x1, y1, x2, y2]
            })

    # 保存结果图像（可选）
    result_image = cv2.imread(image_path)
    for det in detections:
        x1, y1, x2, y2 = map(int, det['bbox'])
        cv2.rectangle(result_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"{det['class_name']} {det['confidence']:.2f}"
        cv2.putText(result_image, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 保存结果
    output_path = os.path.join('static/results', os.path.basename(image_path))
    cv2.imwrite(output_path, result_image)

    return {
        'detections': detections,
        'count': len(detections)
    }