# IMPORTAR LA CLASE YOLO #
from ultralytics import YOLO

# MODELO QUE SE USARÁ COMO PARTIDA #
model = YOLO('yolov8n.pt')

# INICIO DEL PROCESO DE ENTRENAMIENTO #
results = model.train(
    data='placas.v1i.yolov8/data.yaml',     # Ruta al archivo YAML que describe el dataset (clases, rutas a imágenes y etiquetas).
    epochs=60,                              # Número de épocas (vueltas completas al dataset).
    imgsz=416,                              # Tamaño de entrada de las imágenes (416x416 píxeles).
    batch=8,                                # Número de imágenes procesadas por lote. 
    name='placas_col',                      # Nombre de la carpeta donde se guardarán los resultados (dentro de runs/detect/).
    device='cpu'                            # Entrenamiento en CPU.
)

# 70% (408) de las imagenes son de entrenamiento.
# 20% (117) de las imágenes son de validación.
# 10% (58) de las imágenes son de prueba final.

# RESULTADOS:
# Precisión (p) = 0.996 = 99.6% --> Detecta correctamente casi todos los objetos que predice, pocos falsos positivos.
# Recall (r) = 1.0 = 100% --> El modelo detecto el 100% de las placas en cada imagen de entrenamiento.
# mAP@0.5 (precisión media promedio) = 0.995 = 99.5% --> El modelo acierta en casi un 100% en la ubicación de los objetos (placas).

