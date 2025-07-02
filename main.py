from scripts.deteccion_emergencia import detect_emergency_vehicle
from scripts.prediccion_congestion import predict_congestion
from scripts.recuento_de_peatones import count_pedestrians
from scripts.ajuste_tiempo_peatonal import calcular_tiempo_verde_peatonal

import cv2
import datetime

def main():
    print("🔵 Sistema de Semáforo Inteligente iniciado.")
    
    # Inicializa la cámara
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 🟥 1. Detección de vehículos de emergencia
        emergencias = detect_emergency_vehicle(frame)
        if emergencias:
            for det in emergencias:
                x, y, w_box, h_box = det['box']
                label = f"{det['class']}:{det['confidence']:.2f}"
                cv2.rectangle(frame, (x, y), (x + w_box, y + h_box), (0, 0, 255), 2)
                cv2.putText(frame, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                print(f"[{datetime.datetime.now()}] 🚨 Emergencia detectada: {label}")

        # 🟢 2. Conteo de peatones
        cantidad_peatones, rects = count_pedestrians(frame)
        print(f"[{datetime.datetime.now()}] 🚶 Peatones detectados: {cantidad_peatones}")

        # Dibujar los rectángulos de peatones en verde
        for (x, y, w_box, h_box) in rects:
            cv2.rectangle(frame, (x, y), (x+w_box, y+h_box), (0, 255, 0), 2)

        # 🟡 3. Cálculo de tiempo verde peatonal
        tiempo_verde = calcular_tiempo_verde_peatonal(cantidad_peatones)
        print(f"[{datetime.datetime.now()}] ⏱️ Tiempo verde sugerido: {tiempo_verde:.1f} segundos")

        # 🔵 4. Predicción de congestión vehicular
        hora_actual = datetime.datetime.now().hour
        dia_semana = datetime.datetime.now().weekday()
        congestion = predict_congestion(50, hora_actual, dia_semana)
        print(f"[{datetime.datetime.now()}] 🚗 Nivel de congestión predicho: {congestion}")

        # Mostrar información adicional en la ventana
        cv2.putText(frame, f"Peatones: {cantidad_peatones}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        cv2.putText(frame, f"Tiempo Verde: {tiempo_verde:.1f}s", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)
        cv2.putText(frame, f"Congestion: {congestion}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,0), 2)

        cv2.imshow("Sistema Semáforo Inteligente", frame)

        # 🔴 Salir con 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("🔴 Sistema finalizado.")

if __name__ == "__main__":
    main()
