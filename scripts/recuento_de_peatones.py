import cv2

# Inicializa el detector HOG para peatones
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

def count_pedestrians(frame, roi=None):
    # Si se desea, recortar región de interés (ROI) al área de cruce peatonal
    if roi is not None:
        x, y, w, h = roi
        frame_roi = frame[y:y+h, x:x+w]
    else:
        frame_roi = frame

    # Detectar personas
    rects, weights = hog.detectMultiScale(frame_roi, winStride=(4,4), padding=(8,8), scale=1.05)

    # Ajustar coordenadas si se usó ROI
    if roi is not None:
        rects = [(x+rx, y+ry, rw, rh) for (rx, ry, rw, rh) in rects]

    return len(rects), rects

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)  # Usa la webcam

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        count, rects = count_pedestrians(frame)

        # Dibujar los rectángulos detectados
        for (x, y, w_box, h_box) in rects:
            cv2.rectangle(frame, (x, y), (x+w_box, y+h_box), (0, 255, 0), 2)

        cv2.putText(frame, f"Peatones: {count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        cv2.imshow("Conteo de Peatones", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
