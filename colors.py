
import cv2
import numpy as np
import serial
import time

# Configuración de la conexión serial con Arduino
arduino = serial.Serial('COM11', 9600)  # Cambia 'COM3' por tu puerto Arduino

time.sleep(2)  # Esperar a que se establezca la conexión

# Definir rangos HSV para una amplia gama de colores
color_ranges = [
    # Rojos
    {'name': 'Rojo', 'lower': np.array([0, 100, 100]), 'upper': np.array([5, 255, 255]), 'rgb': (0, 0, 255)},
    {'name': 'Rojo', 'lower': np.array([170, 100, 100]), 'upper': np.array([180, 255, 255]), 'rgb': (0, 0, 255)},
    
    # Naranjas
    {'name': 'Naranja', 'lower': np.array([6, 100, 100]), 'upper': np.array([20, 255, 255]), 'rgb': (0, 165, 255)},
    
    # Amarillos
    {'name': 'Amarillo', 'lower': np.array([21, 100, 100]), 'upper': np.array([35, 255, 255]), 'rgb': (0, 255, 255)},
    
    # Verdes
    {'name': 'Verde', 'lower': np.array([36, 50, 50]), 'upper': np.array([85, 255, 255]), 'rgb': (0, 255, 0)},
    
    # Azules
    {'name': 'Azul', 'lower': np.array([86, 100, 100]), 'upper': np.array([120, 255, 255]), 'rgb': (255, 0, 0)},
    
    # Violetas/Magenta
    {'name': 'Violeta', 'lower': np.array([121, 100, 100]), 'upper': np.array([140, 255, 255]), 'rgb': (238, 130, 238)},
    {'name': 'Rosa', 'lower': np.array([141, 100, 100]), 'upper': np.array([169, 255, 255]), 'rgb': (203, 192, 255)},
    
    # Colores acromáticos
    {'name': 'Blanco', 'lower': np.array([0, 0, 200]), 'upper': np.array([180, 50, 255]), 'rgb': (255, 255, 255)},
    {'name': 'Gris', 'lower': np.array([0, 0, 50]), 'upper': np.array([180, 50, 200]), 'rgb': (128, 128, 128)},
    {'name': 'Negro', 'lower': np.array([0, 0, 0]), 'upper': np.array([180, 255, 50]), 'rgb': (0, 0, 0)},
]

def get_color_info(hsv_pixel):
    h, s, v = hsv_pixel
    
    # Primero verificar colores acromáticos
    if v < 50:
        return {'name': 'Negro', 'rgb': (0, 0, 0)}
    elif s < 50 and v > 200:
        return {'name': 'Blanco', 'rgb': (255, 255, 255)}
    elif s < 50 and 50 <= v <= 200:
        return {'name': 'Gris', 'rgb': (128, 128, 128)}
    
    # Luego verificar colores cromáticos
    for color in color_ranges[:-3]:  # Excluir los acromáticos ya verificados
        if cv2.inRange(np.uint8([[hsv_pixel]]), color['lower'], color['upper']): 
            return {'name': color['name'], 'rgb': color['rgb']}
    
    return {'name': 'Desconocido', 'rgb': (128, 128, 128)}

def send_to_arduino(color_name, r, g, b):
    message = f"{color_name},{r},{g},{b}\n"
    arduino.write(message.encode())

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read() 
    if not ret:
        break

    # Punto central
    height, width, _ = frame.shape
    cx, cy = width // 2, height // 2

    # Convertir a HSV y obtener el pixel central
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_pixel = hsv[cy, cx]
    color_info = get_color_info(hsv_pixel)
    
    # Enviar datos a Arduino
    r, g, b = color_info['rgb']
    send_to_arduino(color_info['name'], r, g, b)

    # Mostrar valores HSV y RGB
    hsv_text = f"H: {hsv_pixel[0]} S: {hsv_pixel[1]} V: {hsv_pixel[2]}"
    rgb_text = f"R: {b} G: {g} B: {r}"
    
    # Dibujar marcador y nombre del color
    cv2.circle(frame, (cx, cy), 10, (0, 0, 0), 2)
    cv2.putText(frame, f'Color: {color_info["name"]}', (cx - 70, cy - 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, hsv_text, (cx - 70, cy - 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(frame, rgb_text, (cx - 70, cy - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    cv2.imshow('Detector de Color con Arduino', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

arduino.close()
cap.release()
cv2.destroyAllWindows()