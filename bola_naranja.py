#!/usr/bin/env python3
# Indica al sistema que use Python 3 para ejecutar este script

import cv2
# Importa OpenCV para manejo de imágenes y video

import numpy as np
# Importa NumPy para operaciones numéricas (arrays, matrices, cálculos)

def main():
    # Función principal del programa

    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    # Abre la cámara por defecto (índice 0)

    if not cap.isOpened():
        print("No se pudo abrir la cámara")
        return
    # Verifica si la cámara se abrió correctamente; si no, termina el programa

    total_count = 0
    # Contador acumulativo de bolas detectadas

    last_seen = False  # bandera para evitar múltiples conteos de la misma bola
    # Permite detectar solo un cruce por bola

    line_x = 300
    # Posición en X de la línea vertical de conteo (ajustable según cámara)

    while True:
        # Bucle principal de captura y procesamiento de video

        ret, frame = cap.read()
        # Captura un frame de la cámara
        # ret = True si la captura fue exitosa
        # frame = imagen capturada

        if not ret:
            break
        # Si no se pudo capturar el frame, salir del bucle

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Convierte la imagen de BGR a HSV para filtrar por color

        lower_orange = np.array([5, 100, 100])
        upper_orange = np.array([20, 255, 255])
        # Define el rango de color naranja en HSV

        mask = cv2.inRange(hsv, lower_orange, upper_orange)
        # Crea una máscara binaria: 255 donde el color está dentro del rango, 0 fuera

        mask = cv2.GaussianBlur(mask, (9, 9), 2)
        # Suaviza la máscara para reducir ruido y bordes irregulares

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
        # Detecta círculos usando el método de Hough sobre la máscara
        # dp = resolución acumulador
        # minDist = distancia mínima entre centros de círculos
        # param1 = umbral para el detector de bordes (Canny)
        # param2 = umbral para aceptar un círculo en el acumulador
        # minRadius y maxRadius = rango de radios en píxeles

        count = 0
        # Contador temporal de círculos detectados en este frame

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            # Convierte las coordenadas y radios a enteros

            for (x, y, r) in circles:
                # Itera sobre cada círculo detectado

                cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
                # Dibuja el contorno del círculo en verde

                cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)
                # Dibuja el centro del círculo en rojo

                count += 1
                # Incrementa el contador de este frame

                cv2.line(frame, (line_x, 0), (line_x, frame.shape[0]), (255, 0, 0), 2)
                # Dibuja la línea vertical azul para el conteo

                if x > line_x and not last_seen:
                    total_count += 1
                    last_seen = True
                elif x <= line_x:
                    last_seen = False
                # Detecta cuando la bola cruza la línea vertical
                # Solo incrementa total_count si no se había contado ya

        cv2.putText(frame, f"Detectadas ahora: {count}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        # Muestra en la pantalla cuántas bolas detecta este frame

        cv2.putText(frame, f"Total acumulado: {total_count}", (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        # Muestra el contador acumulativo total

        cv2.imshow("Contador de Bolas Naranjas", frame)
        # Muestra la ventana con el frame procesado

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # Sale del bucle si se presiona la tecla 'q'

    cap.release()
    # Libera la cámara

    cv2.destroyAllWindows()
    # Cierra todas las ventanas de OpenCV

if __name__ == "__main__":
    main()
# Llama a la función principal si se ejecuta el script directamente
