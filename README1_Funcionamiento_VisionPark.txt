VISIONPARK - FUNCIONAMIENTO GENERAL


VisionPark es un sistema inteligente de reconocimiento de placas vehiculares que permite el control de acceso
en un conjunto residencial. El sistema funciona en tiempo real usando visión por computador, OCR y una base 
de datos en Excel para registrar y verificar vehículos.


1. INICIO DE SESIÓN (SEGURIDAD)

- Al ejecutar el sistema, se abre una ventana de login.
- El usuario debe autenticarse con su nombre de usuario y contraseña.
- Estos datos se verifican contra el archivo Excel 'Autorizados.xlsx'.
- Si la autenticación es correcta, se registra la hora y fecha de ingreso y se inicia el sistema de detección.


2. DETECCIÓN DE PLACA

- Se activa la cámara en tiempo real.
- Se utiliza un modelo YOLOv8 entrenado para detectar automáticamente la ubicación de placas.
- Cuando una placa es detectada, se recorta la región de interés (ROI) y se muestra al usuario.
- Después de 2 segundos de estabilización, se aplica preprocesamiento de imagen y se extrae el texto de la placa con EasyOCR.


3. CONFIRMACIÓN DE LA PLACA

- Se muestra una ventana que pregunta al usuario: "¿Esta es su placa?" con el texto detectado.
- Si el usuario confirma, el sistema continúa; si no, reinicia el estado y vuelve a buscar.


4. VERIFICACIÓN EN EXCEL

- Si la placa está registrada en 'vehiculos' (Re_vehiculos.xlsx), se registra el ingreso en la hoja 'registro'.
- Si la placa NO está registrada, se abre una ventana para registrar los datos como visitante:
  - Nombre completo
  - Documento
  - Marca del vehículo
  - Apartamento destino
- El visitante también queda registrado en la hoja 'registro'.


5. CONTROL DEL SISTEMA

- En paralelo, hay una ventana flotante con un botón "Salir del sistema".
- Si el usuario cierra la ventana o presiona el botón, el sistema se detiene completamente.
- También puede cerrarse si se cierra la ventana principal de video.


6. FUNCIONALIDADES CLAVE

* Reconocimiento automático de placas
* Confirmación visual al usuario
* Registro histórico de ingresos
* Registro de visitantes
* Doble autenticación por usuario autorizado
* Operación con archivos Excel (sin necesidad de SQL Server)


7. LIMITACIONES

- OCR puede fallar si la imagen es muy borrosa o la placa está en ángulo extremo.
- El sistema depende de una buena iluminación.
- El rendimiento depende de las capacidades del hardware.


8. RECOMENDACIONES

- Ejecutar en un entorno con buena iluminación y fondo neutro.
- Mantener los archivos 'Re_vehiculos.xlsx' y 'Autorizados.xlsx' en el mismo directorio del sistema.
- No modificar la estructura de columnas de los archivos Excel.
- Mantener actualizado el modelo YOLO con nuevas imágenes si hay cambios en las placas.

