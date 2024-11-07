import time
import threading
import queue
import random

# Parámetros del sistema
FRAMES_PER_SECOND = 30
PROCESSING_DELAY = 0.01
NETWORK_BANDWIDTH = 10
BUFFER_SIZE = 50

# Cola para el buffer de almacenamiento temporal
buffer = queue.Queue(maxsize=BUFFER_SIZE)

# Función de captura y codificación de video
def video_capture():
    while True:
        time.sleep(1 / FRAMES_PER_SECOND)
        frame = f"Frame-{random.randint(1, 1000)}"
        try:
            buffer.put(frame, timeout=0.1)
            print(f"[Captura] {frame} capturado y añadido al buffer.")
        except queue.Full:
            print("[Advertencia] Buffer lleno. Pérdida de frames.")
            continue

# Función de transmisión de video
def video_transmission():
    while True:
        time.sleep(1 / NETWORK_BANDWIDTH)
        try:
            frame = buffer.get(timeout=0.1)
            print(f"[Transmisión] {frame} transmitido al cliente.")
            buffer.task_done()
        except queue.Empty:
            print("[Advertencia] Esperando más frames en el buffer.")

# Simulación de clientes recibiendo datos
def client_simulator():
    while True:
        time.sleep(0.05)
        print("[Cliente] Frame recibido y reproducido.")

# Crear hilos para cada componente
capture_thread = threading.Thread(target=video_capture)
transmission_thread = threading.Thread(target=video_transmission)
client_thread = threading.Thread(target=client_simulator)

# Iniciar los hilos
capture_thread.start()
transmission_thread.start()
client_thread.start()

# Esperar a que finalicen los hilos
capture_thread.join()
transmission_thread.join()
client_thread.join()
