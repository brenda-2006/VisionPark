# LIBRERIAS NECESARIAS #
import pyodbc

# Función para conectar al servidor SQL Server.
def conectar_sql_server(nombre_bd):
    try:
        # Configuración de la conexión a SQL Server usando autenticación de Windows.
        conn = pyodbc.connect(
            "Driver={SQL Server};"                  # Usa el driver de SQL Server instalado en el sistema.
            "Server=DESKTOP-KMG57VB\SQLEXPRESS;"    # Nombre del servidor + instancia de SQL Server.
            f"Database={nombre_bd};"                # Nombre de la base de datos.
            "Trusted_Connection=yes;"               # Usa las credenciales del usuario de Windows.
        )
        print(f"\nConexión con SQL Server establecida.\nBase de datos: {nombre_bd}\n\n")
        return conn     # Retornamos la conexión.
    
    except Exception as e:      # Mostramos un error si ocurre algún problema.
        print(f"Error al conectar con SQL Server: {e}")  
        return None

# Conexión a la base de datos de vehículos del conjunto.
conn1 = conectar_sql_server("VehiculosConjunto")

# Conexión a la base de datos de usuarios autorizados.
conn2 = conectar_sql_server("UsuariosAutorizados")