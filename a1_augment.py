# LIBRERIAS #
import os                       # Para trabajar con rutas de archivos y carpetas.
import cv2                      # Para leer y guardar las imágenes.
import albumentations as A      # Librería para realizar aumentos de datos.
from tqdm import tqdm           # Visualización del avance que se realiza.

# RUTA DONDE ESTÁN LAS CARPETAS DE IMÁGENES Y ETIQUETAS #
BASE_DIR = r'd:\Desktop\IA\Proyecto_final\placas.v1i.yolov8'

# RUTAS ORIGINALES #
IMG_DIR = os.path.join(BASE_DIR, 'train', 'images')
LABEL_DIR = os.path.join(BASE_DIR, 'train', 'labels')

# NUEVAS RUTAS PARA EL AUMENTO Y SUS ETIQUETAS #
AUG_IMG_DIR = os.path.join(BASE_DIR, 'train', 'images_aug')
AUG_LABEL_DIR = os.path.join(BASE_DIR, 'train', 'labels_aug')

# CREAR LA CARPETA (SI NO EXISTE) #
os.makedirs(AUG_IMG_DIR, exist_ok=True)
os.makedirs(AUG_LABEL_DIR, exist_ok=True)

# TRANSFORMACIONES ALEATORIAS PARA AUMENTAR LOS DATOS #
transform = A.Compose([
    A.Rotate(limit=25, p=0.5),              # Rotación aleatoria hasta ±25°.
    A.RandomBrightnessContrast(p=0.5),      # Cambios en el brillo y contraste.
    A.GaussianBlur(p=0.3),                  # Desenfoque Gaussiano.
    A.RandomFog(p=0.2),                     # Niebla aleatoriamente.
    A.RandomRain(p=0.2),                    # Efecto de lluva.
    A.MotionBlur(p=0.3),                    # Desenfoque por movimiento.
    A.RandomScale(scale_limit=0.2, p=0.3),  # Escalado aleatorio hasta ±20%.
    A.HorizontalFlip(p=0.3)                 # Volteo horizontal.
], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))      # Configuración: cómo se transforman las cajas.

# APLICAR AUMENTACIÓN EN CADA IMAGEN #
for img_name in tqdm(os.listdir(IMG_DIR)):
    if not img_name.endswith('.jpg') and not img_name.endswith('.png'):     # Verifica que el archivo sea una imagen válida.
        continue
    
    # Construye la ruta completa de la imagen y su archivo de etiquetas.
    img_path = os.path.join(IMG_DIR, img_name)
    label_path = os.path.join(LABEL_DIR, img_name.replace('.jpg', '.txt').replace('.png', '.txt'))

    # Si no existe el archivo de etiquetas correspondiente, se salta.
    if not os.path.exists(label_path):
        continue

     # Carga la imagen.
    image = cv2.imread(img_path)
    h, w = image.shape[:2]

    # Lee las etiquetas del archivo .txt
    with open(label_path, 'r') as f:
        lines = f.read().splitlines()

    bboxes = []         # Lista de cajas.
    labels = []         # Lista de clases correspondientes.

    for line in lines:
        parts = line.strip().split()
        if len(parts) != 5:
            continue
        cls = int(parts[0])                     # Clase.
        x, y, bw, bh = map(float, parts[1:])    # Coordenadas y tamaño de la caja.
        bboxes.append([x, y, bw, bh])           # Añade la caja.
        labels.append(cls)                      # Añade la clase.

    # Aumentar 3 veces cada imagen.
    for i in range(3):
        try:
            # Aplica las transformaciones.
            augmented = transform(image=image, bboxes=bboxes, class_labels=labels)
            aug_img = augmented['image']             # Imagen aumentada.
            aug_bboxes = augmented['bboxes']         # Nuevas cajas transformadas.
            aug_labels = augmented['class_labels']   # Etiquetas correspondientes.

            # Nombres nuevos para las imágenes y etiquetas generadas.
            new_img_name = img_name.replace('.jpg', f'_aug{i}.jpg').replace('.png', f'_aug{i}.jpg')
            new_lbl_name = img_name.replace('.jpg', f'_aug{i}.txt').replace('.png', f'_aug{i}.txt')

            # Guarda la nueva imagen aumentada.
            cv2.imwrite(os.path.join(AUG_IMG_DIR, new_img_name), aug_img)

            # Guarda las etiquetas correspondientes en formato YOLO.
            with open(os.path.join(AUG_LABEL_DIR, new_lbl_name), 'w') as f:
                for cls, bbox in zip(aug_labels, aug_bboxes):
                    f.write(f"{cls} {' '.join(map(str, bbox))}\n")
                    
        except Exception as e:
            print(f"Error con {img_name}: {e}")
