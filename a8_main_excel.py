# LIBRERIAS NECESARIAS #
import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import datetime
from a7_deteccion_excel import iniciar_deteccion

# FUNCIONES PARA EXCEL DE USUARIOS #

# Leer hoja de Autorizados.xlsx
def leer_hoja_autorizados(nombre_hoja):
    return pd.read_excel("Autorizados.xlsx", sheet_name=nombre_hoja)

# Guardar en hoja de Autorizados.xlsx
def guardar_en_hoja_autorizados(df, nombre_hoja):
    libro = pd.read_excel("Autorizados.xlsx", sheet_name=None)      # Carga todas las hojas del archivo.
    libro[nombre_hoja] = df         # Reemplaza el contenido de la hoja deseada.
    with pd.ExcelWriter("Autorizados.xlsx", engine="openpyxl", mode="w") as writer:
        for hoja, contenido in libro.items():
            contenido.to_excel(writer, sheet_name=hoja, index=False)        # Guarda cada hoja sin el índice.

# Verifica credenciales con la hoja "autorizados".
def verificar_credenciales_excel(usuario, contrasena):
    df = leer_hoja_autorizados("autorizados")       # Lee la hoja con usuarios registrados.

    # Limpia los datos del Excel.
    df["Usuario."] = df["Usuario."].astype(str).str.strip().str.lower()
    df["Contraseña."] = df["Contraseña."].apply(lambda x: str(x).zfill(4))      # Asegura 4 dígitos.

    # Limpia los datos ingresados.
    usuario = usuario.strip().lower()
    contrasena = contrasena.strip()

    # Devuelve True si se encuentra un usuario con la contraseña correspondiente.
    return ((df["Usuario."] == usuario) & (df["Contraseña."] == contrasena)).any()

# Registra la sesión en hoja "registros".
def registrar_inicio_sesion(usuario):
    fecha = datetime.now().strftime("%Y-%m-%d")         # Fecha actual.
    hora = datetime.now().strftime("%H:%M:%S")          # Hora actual.
    df = leer_hoja_autorizados("registros")             # Lee hoja de sesiones.
    nueva = pd.DataFrame([[usuario, fecha, hora]], columns=df.columns)      # Nueva fila.
    df = pd.concat([df, nueva], ignore_index=True)      # Agrega al final.
    guardar_en_hoja_autorizados(df, "registros")        # Guarda nuevamente.

# INTERFAZ DE LOGIN #

# Crea la ventana de login
def crear_login():
    # Función que se ejecuta al presionar el botón "Iniciar sesión"
    def iniciar_sesion():
        usuario = entry_usuario.get()           # Obtiene texto del campo de usuario.
        contrasena = entry_contrasena.get()     # Obtiene texto del campo de contraseña.

        if verificar_credenciales_excel(usuario, contrasena):       # Verifica con Excel.
            messagebox.showinfo("Acceso permitido", f"Bienvenido, {usuario}!")      # Muestra bienvenida.
            registrar_inicio_sesion(usuario)        # Registra fecha/hora del login
            ventana.destroy()                       # Cierra ventana de login.
            iniciar_deteccion()                      # Inicia sistema principal (detección).

        else:
            messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos")

    # Configuración de la ventana principal del login.
    ventana = tk.Tk()
    ventana.title("Inicio de sesión - VisionPark")      # Título de la ventana
    ventana.geometry("400x300")                         # Tamaño en píxeles.
    ventana.config(bg="#e6f2ff")                      # Color de fondo.

    # Widgets: etiquetas, campos de texto y botón.
    tk.Label(ventana, text="Autenticación de Usuario", font=("Arial", 14, "bold"), bg="#e6f2ff").pack(pady=10)
    tk.Label(ventana, text="Usuario:", bg="#e6f2ff").pack()
    entry_usuario = tk.Entry(ventana, width=30)     # Campo para escribir el usuario.
    entry_usuario.pack(pady=5)
    tk.Label(ventana, text="Contraseña:", bg="#e6f2ff").pack()
    entry_contrasena = tk.Entry(ventana, show="*", width=30)        # Campo de contraseña oculta.
    entry_contrasena.pack(pady=5)

    # Botón para iniciar sesión.
    tk.Button(ventana, text="Iniciar sesión", command=iniciar_sesion, bg="#0066cc", fg="white").pack(pady=20)

    # Inicia el bucle principal de la interfaz.
    ventana.mainloop()

# INICIO DEL SISTEMA #
# Si se ejecuta directamente el script, lanza la interfaz de login.
if __name__ == "__main__":
    crear_login()
