# LIBRERIAS NECESARIAS #
import cv2                          # Para capturar y mostrar video en tiempo real
import time                         # Para manejar tiempos de espera
import pandas as pd                 # Para leer y escribir en archivos Excel
import easyocr                      # OCR basado en deep learning para detectar texto
from datetime import datetime       # Para obtener fecha y hora actuales
from tkinter import Tk, messagebox, Toplevel, Label, Entry, Button  # Para interfaz de usuario
from ultralytics import YOLO        # Modelo YOLOv8 para detección de placas
from a3_preprocesamiento import preprocesar_placa  # Función para mejorar la imagen antes del OCR
import sys                          # Para cerrar el sistema completamente


# Inicializa OCR
reader = easyocr.Reader(['en'], gpu=False)


#--------------------------------------------- Carga modelo YOLO------------------------------------------------------------#
#------------------ PARA USAR EN OTRA PC, SE DEBE MODIFICAR LA RUTA DONDE SE ENCUENTRA EL MODELO ENTRENADO------------------#

modelo = YOLO(r"D:\Desktop\IA\Proyecto_final\runs\detect\placas_col\weights\best.pt")

#----------------------------------------------------------------------------------------------------------------------------#



# Oculta ventana principal
Tk().withdraw()

######## FUNCIONES PARA EXCEL ########

# Función para leer una hoja del libro Re_vehiculos.xlsx
def leer_hoja(nombre_hoja):
    return pd.read_excel("Re_vehiculos.xlsx", sheet_name=nombre_hoja)

# Función para guardar datos en una hoja específica
def guardar_en_hoja(df, nombre_hoja):
    libro = pd.read_excel("Re_vehiculos.xlsx", sheet_name=None)         # Carga todas las hojas.
    libro[nombre_hoja] = df         # Reemplaza la hoja específica
    with pd.ExcelWriter("Re_vehiculos.xlsx", engine="openpyxl", mode="w") as writer:
        for hoja, contenido in libro.items():
            contenido.to_excel(writer, sheet_name=hoja, index=False)

# Verifica si una placa ya está registrada en la hoja "vehiculos"
def esta_registrado(placa):
    df = leer_hoja("vehiculos")
    placas_excel = df["Placa."].astype(str).str.strip().str.upper()
    placa_limpia = placa.strip().upper()
    return placa_limpia in placas_excel.values


######## FUNCIONES PARA REGISTRO ########

# Registrar ingreso en hoja "registro"
def registrar_ingreso(placa):
    df = leer_hoja("vehiculos")
    fila = df[df["Placa."] == placa].iloc[0]
    nombre = fila["Nombre."]
    marca = fila["Marca."]

    fecha = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M:%S")

    df_registro = leer_hoja("registro")
    nueva = pd.DataFrame([[placa, fecha, hora, nombre, marca]], columns=df_registro.columns)
    df_registro = pd.concat([df_registro, nueva], ignore_index=True)
    guardar_en_hoja(df_registro, "registro")
    print("✅ Registro de ingreso guardado.")

# Registrar visitante si la placa no está en "vehiculos"
def registrar_visitante_interfaz(placa_detectada, callback_reiniciar):
    def guardar():
        placa = placa_detectada
        nombre = entry_nombre.get()
        documento = entry_doc.get()
        marca = entry_marca.get()
        destino = entry_destino.get()
        fecha = datetime.now().strftime("%Y-%m-%d")
        hora = datetime.now().strftime("%H:%M:%S")

        df_visita = leer_hoja("visitantes")
        nueva = pd.DataFrame([[placa, nombre, documento, marca, destino, fecha, hora]],
                             columns=df_visita.columns)
        df_visita = pd.concat([df_visita, nueva], ignore_index=True)
        guardar_en_hoja(df_visita, "visitantes")

        df_registro = leer_hoja("registro")
        nueva_reg = pd.DataFrame([[placa, fecha, hora, nombre, marca]],
                                 columns=df_registro.columns)
        df_registro = pd.concat([df_registro, nueva_reg], ignore_index=True)
        guardar_en_hoja(df_registro, "registro")

        print("📝 Visitante registrado y acceso concedido.")
        ventana.quit()
        ventana.destroy()
        callback_reiniciar()        # Reinicia el sistema de detección

    ventana = Toplevel()
    ventana.title("Registro visitante")

    def cerrar_ventana():
        ventana.quit()
        ventana.destroy()
        callback_reiniciar()

    ventana.protocol("WM_DELETE_WINDOW", cerrar_ventana)


    Label(ventana, text=f"Placa detectada: {placa_detectada}").grid(row=0, column=0, columnspan=2)

    Label(ventana, text="Nombre completo:").grid(row=1, column=0)
    entry_nombre = Entry(ventana)
    entry_nombre.grid(row=1, column=1)

    Label(ventana, text="Documento:").grid(row=2, column=0)
    entry_doc = Entry(ventana)
    entry_doc.grid(row=2, column=1)

    Label(ventana, text="Marca:").grid(row=3, column=0)
    entry_marca = Entry(ventana)
    entry_marca.grid(row=3, column=1)

    Label(ventana, text="Apartamento destino:").grid(row=4, column=0)
    entry_destino = Entry(ventana)
    entry_destino.grid(row=4, column=1)

    Button(ventana, text="Registrar y Dar Ingreso", command=guardar).grid(row=5, column=0, columnspan=2)
    ventana.mainloop()

######## FUNCIONES OCR ########

# OCR con EasyOCR
def detectar_texto(imagen_preprocesada):
    resultado = reader.readtext(imagen_preprocesada, detail=0)
    if resultado:
        texto_limpio = ''.join(filter(str.isalnum, resultado[0]))
        return texto_limpio.upper()
    return None


######## PROCESO PRINCIPAL ########

# Proceso principal
def iniciar_deteccion():
    salir_flag = [False]  # usamos lista para poder modificar desde función interna
    cap = cv2.VideoCapture(0)       # Captura desde cámara.
    estado = "buscando"
    texto_detectado = None
    tiempo_inicio = None
    coordenadas = None

    def reiniciar_estado():
        nonlocal estado, texto_detectado, tiempo_inicio, coordenadas
        estado = "buscando"
        texto_detectado = None
        tiempo_inicio = None
        coordenadas = None
    
    # Ventana de control con botón Salir
    ventana_control = Tk()
    ventana_control.title("Control")
    ventana_control.geometry("200x100")
    ventana_control.configure(bg="#ffecec")

    def cerrar_todo():
        salir_flag[0] = True
        ventana_control.destroy()
        cap.release()
        cv2.destroyAllWindows()
        print("✅ Sistema cerrado manualmente.")
        sys.exit()  # <- Esto detiene completamente el programa

    boton_salir = Button(ventana_control, text="❌ Salir del sistema", command=cerrar_todo, bg="red", fg="white")
    boton_salir.pack(pady=20)

    # Ejecutar la ventana en segundo plano
    ventana_control.update()


    while True:
        ventana_control.update()  # mantiene viva la ventana del botón
        if salir_flag[0]:
            break

        ret, frame = cap.read()
        if not ret:
            break

        resultado = modelo.predict(source=frame, conf=0.5, imgsz=416, verbose=False)
        detecciones = resultado[0].boxes

        if detecciones is not None and len(detecciones) > 0:
            if estado == "buscando":
                tiempo_inicio = time.time()
                estado = "esperando"

            box = detecciones[0]
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(frame.shape[1], x2), min(frame.shape[0], y2)
            coordenadas = (x1, y1, x2, y2)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, "Placa detectada", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        if estado == "esperando" and coordenadas and time.time() - tiempo_inicio >= 2 and texto_detectado is None:
            x1, y1, x2, y2 = coordenadas
            roi = frame[y1:y2, x1:x2]
            imagen_pre = preprocesar_placa(roi)
            texto_detectado = detectar_texto(imagen_pre)

            if texto_detectado:
                estado = "verificando"
            else:
                print("⚠️ No se pudo leer texto.")
                estado = "buscando"
                tiempo_inicio = None
                coordenadas = None

        if estado == "verificando":
            respuesta = messagebox.askyesno("Confirmar placa", f"¿Esta es su placa?\n\n{texto_detectado}")
            if respuesta:
                if esta_registrado(texto_detectado):
                    registrar_ingreso(texto_detectado)
                else:
                    registrar_visitante_interfaz(texto_detectado, reiniciar_estado)
            else:
                print("❌ Usuario rechazó la placa.")

            estado = "buscando"
            texto_detectado = None
            tiempo_inicio = None
            coordenadas = None

        cv2.imshow("VisionPark (modo Excel)", frame)
        if cv2.getWindowProperty("VisionPark (modo Excel)", cv2.WND_PROP_VISIBLE) < 1:
            print("🛑 Ventana cerrada. Cerrando sistema...")
            break


    cap.release()
    cv2.destroyAllWindows()

# MAIN
if __name__ == "__main__":
    iniciar_deteccion()
