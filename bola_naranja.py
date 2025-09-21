import cv2
import numpy as np

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("No se pudo abrir la cámara")
        return

    total_count = 0
    last_seen = False  # bandera para evitar múltiples conteos de la misma bola

    # Posición de la línea vertical (ajusta según tu cámara)
    line_x = 300

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_orange = np.array([5, 100, 100])
        upper_orange = np.array([20, 255, 255])
        mask = cv2.inRange(hsv, lower_orange, upper_orange)
        mask = cv2.GaussianBlur(mask, (9, 9), 2)

        circles = cv2.HoughCircles(
            mask,
            cv2.HOUGH_GRADIENT,
            dp=1.2,
            minDist=200,
            param1=50,
            param2=30,
            minRadius=20,
            maxRadius=100
        )

        count = 0
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
                cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)
                count += 1

                # Dibujar línea vertical
                cv2.line(frame, (line_x, 0), (line_x, frame.shape[0]), (255, 0, 0), 2)

                # Detectar cruce en X
                if x > line_x and not last_seen:
                    total_count += 1
                    last_seen = True
                elif x <= line_x:
                    last_seen = False  # reset cuando ya pasó

        # Mostrar datos
        cv2.putText(frame, f"Detectadas ahora: {count}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(frame, f"Total acumulado: {total_count}", (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("Contador de Bolas Naranjas", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
