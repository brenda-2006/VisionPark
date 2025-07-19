# LIBRERIAS NECESARIAS #
from ultralytics import YOLO                                            # Para usar el modelo YOLOv8.       
import cv2                                                              # Para capturar y mostrar video en tiempo real.
from a3_preprocesamiento import preprocesar_placa, detectar_texto       # Funciones OCR personalizadas.
import pyodbc                                                           # Para conectarse a SQL Server.
from datetime import datetime                                           # Para obtener fecha y hora actual.
from tkinter import messagebox, Tk                                      # Para mostrar ventana de confirmación al usuario.
import time                                                             # Para controlar el tiempo entre eventos.

# Oculta la ventana principal de Tkinter (usamos solo los cuadros de diálogo).
Tk().withdraw()

# CONEXIÓN A SQL SERVER #
def conectar_sql_server():
    try:
        conn = pyodbc.connect(
            "Driver={SQL Server};"
            "Server=DESKTOP-KMG57VB\\SQLEXPRESS;"
            "Database=VehiculosConjunto;"
            "Trusted_Connection=yes;"
        )
        print("✅ Conexión exitosa a SQL Server.")
        return conn
    
    except Exception as e:
        print(f"❌ Error conectando a SQL Server: {e}")
        return None

# REGISTRAR DETECCIÓN #
def registrar_deteccion(conn, placa):
    fecha = datetime.now().strftime("%Y-%m-%d")     # Fecha actual.
    hora = datetime.now().strftime("%H:%M:%S")      # Hora actual.

    # Verificar que la placa tenga sentido.
    if not placa or len(placa) < 5:
        print("⚠️ Placa no válida. No se guarda.")
        return

    try:
        cursor = conn.cursor()

        # Insertar registro en la tabla Detección.
        cursor.execute(
            "INSERT INTO Deteccion (Placa, Fecha_in, Hora_in) VALUES (?, ?, ?)",
            (placa, fecha, hora)
        )
        conn.commit()
        print(f"✅ Registro guardado: {placa} - {fecha} {hora}")

    except Exception as e:
        print(f"❌ Error al guardar: {e}")

# CARGAR MODELO YOLOv8 #
model = YOLO(r"D:\Desktop\IA\Proyecto_final\runs\detect\placas_col\weights\best.pt")

# CAPTURA DE VIDEO #
def iniciar_deteccion(conn):

    # Usar cámara del computador por defecto.
    cap = cv2.VideoCapture(0)     
    
    # Variables de control de estado.
    tiempo_inicio = None
    coordenadas_placa = None
    texto_detectado = None
    estado = "buscando"

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detección en vivo.
        resultados = model.predict(source=frame, conf=0.5, imgsz=416, verbose=False)
        detecciones = resultados[0].boxes

        if detecciones is not None and len(detecciones) > 0:
            if estado == "buscando":
                tiempo_inicio = time.time()     # Marca tiempo para OCR
                estado = "esperando"

            box = detecciones[0]
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            h, w = frame.shape[:2]

            # Limitar coordenadas dentro del frame.
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)
            coordenadas_placa = (x1, y1, x2, y2)

            # Dibujar caja verde en la imagen.
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, "Placa detectada", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Esperar 2 segundos y luego intenta OCR.
        if estado == "esperando" and coordenadas_placa and time.time() - tiempo_inicio >= 2 and texto_detectado is None:

            x1, y1, x2, y2 = coordenadas_placa
            roi = frame[y1:y2, x1:x2]         # Extraer la región de la placa.

            cv2.imshow("ROI capturado", roi)  # Ver el ROI visualmente.
            cv2.waitKey(500)

            imagen_placa = preprocesar_placa(roi)           # Aplicar filtros para OCR.
            texto_detectado = detectar_texto(imagen_placa)  # Extraer texto con EasyOCR.

            if texto_detectado:
                estado = "verificando"
            else:
                print("⚠️ OCR no encontró texto.")
                estado = "buscando"
                tiempo_inicio = None
                texto_detectado = None   # Reinicia también esto
                coordenadas_placa = None # Esto es clave para volver a detectar desde 0

        # CONFIRMAR PLACA #
        if estado == "verificando":
            if texto_detectado:
                print(f"🔎 Mostrando confirmación: {texto_detectado}")
                respuesta = messagebox.askyesno("¿Confirmar Placa?", f"¿Esta es su placa?\n\n{texto_detectado}")
                if respuesta:
                    registrar_deteccion(conn, texto_detectado)
                else:
                    print("❌ Usuario rechazó la placa")
            else:
                print("⚠️ OCR no encontró texto.")

            # Siempre reiniciamos el estado, haya o no haya texto.
            estado = "buscando"
            texto_detectado = None
            tiempo_inicio = None
            coordenadas_placa = None


        # Mostrar video en tiempo real.
        cv2.imshow("VisionPark - En tiempo real", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Liberar cámara y cerrar ventanas.
    cap.release()
    cv2.destroyAllWindows()

# MAIN #
if __name__ == "__main__":
    conn = conectar_sql_server()
    if conn:
        iniciar_deteccion(conn)
    else:
        print("❌ No se pudo iniciar el sistema.")


