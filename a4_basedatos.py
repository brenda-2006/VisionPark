# LIBRERIAS NECESARIAS #
from datetime import datetime

# Función que guarda en la base de datos una nueva entrada de detección vehicular.
def guardar_en_base_de_datos(conn, placa):
    try:
        # Crear un cursor para ejecutar comandos SQL sobre la conexión existente.
        cursor = conn.cursor()

        # Obtener la fecha y hora actual del sistema.
        fecha_actual = datetime.now().date()
        hora_actual = datetime.now().time()

        # Buscar el nombre y parqueadero si está en VehiculosRegistrados (base de datos).
        cursor.execute("SELECT Nombre, Marca, Num_Parqueadero FROM VehiculosRegistrados WHERE Placa = ?", placa)
        vehiculo = cursor.fetchone()

        if vehiculo:
            # Si se encontró el vehículo en VehiculosRegistrados, extrae la info
            nombre, marca, parqueadero = vehiculo
        else:
            # # Si no está registrado, busca en la tabla de visitas.
            cursor.execute("SELECT Nombre, Marca FROM VehiculosVisita WHERE Placa = ?", placa)
            vehiculo_visita = cursor.fetchone()

            if vehiculo_visita:
                # Si lo encuentra como visitante, guarda nombre y marca.
                nombre, marca = vehiculo_visita
                parqueadero = None

            else:
                # Si no está en ninguna tabla, se registra como desconocido.
                nombre = "Desconocido"
                marca = "Desconocida"
                parqueadero = None

        # Insertar en tabla Detección
        cursor.execute("""
            INSERT INTO Deteccion (Placa, Fecha_in, Hora_in, Nombre, Marcar, Num_Parqueadero)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (placa, fecha_actual, hora_actual, nombre, marca, parqueadero)
        )

        # Confirmar los cambios en la base de datos.
        conn.commit()

        # Confirmación por consola
        print("✅ Registro guardado en base de datos")

    except Exception as e:
        # Captura cualquier error durante el proceso y lo muestra
        print(f"❌ Error al guardar en la base de datos: {e}")
