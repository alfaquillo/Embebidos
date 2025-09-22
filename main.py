#!/usr/bin/env python3 
import cv2
import numpy as np

def main():
    # Abrir la cámara (0 = cámara por defecto)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("No se pudo abrir la cámara")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convertir a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Suavizar para reducir ruido
        gray = cv2.GaussianBlur(gray, (9, 9), 2)

        # Detectar círculos usando HoughCircles
        circles = cv2.HoughCircles(
            gray,
            cv2.HOUGH_GRADIENT,
            dp=1.2,
            minDist=30,
            param1=50,
            param2=30,
            minRadius=10,
            maxRadius=80
        )

        count = 0
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            count = len(circles)

            for (x, y, r) in circles:
                cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
                cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)

        # Mostrar contador en pantalla
        cv2.putText(frame, f"Bolas detectadas: {count}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Mostrar la imagen
        cv2.imshow("Deteccion de Bolas", frame)

        # Salir con 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
