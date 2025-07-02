import cv2
import numpy as np

# Configura la ruta a tus archivos YOLOv4-tiny o MobileNet SSD
MODEL_CONFIG = 'models/yolov4-tiny.cfg'
MODEL_WEIGHTS = 'models/yolov4-tiny.weights'
CLASSES_FILE = 'models/classes.names'

# Carga las clases
with open(CLASSES_FILE, 'r') as f:
    classes = [line.strip() for line in f.readlines()]

# Inicializa la red DNN de OpenCV
net = cv2.dnn.readNetFromDarknet(MODEL_CONFIG, MODEL_WEIGHTS)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)  # Cambia a DNN_TARGET_CUDA si tienes GPU

def detect_emergency_vehicle(frame, conf_threshold=0.5, nms_threshold=0.4):
    h, w = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    # Nombres de capas de salida
    ln = net.getUnconnectedOutLayersNames()
    outputs = net.forward(ln)

    boxes = []
    confidences = []
    classIDs = []

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = float(scores[classID])

            if confidence > conf_threshold and classes[classID] in ['ambulance', 'fire_truck', 'police']:
                box = detection[0:4] * np.array([w, h, w, h])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                boxes.append([x, y, int(width), int(height)])
                confidences.append(confidence)
                classIDs.append(classID)

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    detections = []

    if len(idxs) > 0:
        for i in idxs.flatten():
            detections.append({
                'class': classes[classIDs[i]],
                'confidence': confidences[i],
                'box': boxes[i]
            })

    return detections

# Ejemplo de prueba directa
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)  # 0 para webcam

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detections = detect_emergency_vehicle(frame)

        for det in detections:
            x, y, w_box, h_box = det['box']
            label = f"{det['class']}:{det['confidence']:.2f}"
            cv2.rectangle(frame, (x, y), (x + w_box, y + h_box), (0, 0, 255), 2)
            cv2.putText(frame, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        cv2.imshow("Detección Vehículo Emergencia", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
