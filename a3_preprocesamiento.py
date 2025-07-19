# LIBRERIAS NECESARIAS #
import cv2          # OpenCV: para procesamiento de imágenes.
import easyocr      # EasyOCR: para reconocimiento óptico de caracteres.
import re           # Expresiones regulares para limpiar y validar el texto.

# Crear lector de EasyOCR con idioma inglés.
reader = easyocr.Reader(['en'], gpu=False)

# Función para preprocesar (simple).
def preprocesar_placa(roi):
    try:
        alto_deseado = 150          # Altura deseada para normalizar el tamaño de la imagen.
        escala = alto_deseado / roi.shape[0]        # Calcular factor de escala.
        roi = cv2.resize(roi, None, fx=escala, fy=escala, interpolation=cv2.INTER_CUBIC)        # Redimensionar

        # Convertir a escala de grises.
        gris = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # Aplicar umbral adaptativo.
        umbral = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 11, 2)

        return umbral       # Devuelve imagen preprocesada.
    
    except Exception as e:

        # En caso de error durante el preprocesamiento
        print("⚠️ Error durante el preprocesamiento:", e)
        return None


# Función para detectar texto usando EasyOCR.
def detectar_texto(img):
    try:
        print("🔎 Iniciando OCR...")
        resultados = reader.readtext(img)       # Aplica OCR a la imagen.
        print("📋 Resultados:", resultados)

        candidatos = []                         # Lista para guardar posibles placas.

        # Procesar cada resultado de OCR (coordenadas, texto, confianza).
        for bbox, texto, confianza in resultados:
            texto_limpio = re.sub(r'[^A-Z0-9]', '', texto.upper())      # Elimina símbolos y deja solo letras y números.

            # Calcula la altura del texto en píxeles.
            altura = abs(bbox[2][1] - bbox[0][1])

            # Filtro: mínimo 5 caracteres, confianza aceptable y altura suficiente.
            if len(texto_limpio) >= 5 and confianza > 0.3 and altura > 10:

                # Buscar patrones de placas tipo ABC123 o similar.
                if re.match(r'^[A-Z]{3}\d{3}$', texto_limpio):
                    candidatos.append((texto_limpio, altura, confianza))
                
                 # O al menos 2 letras y 2 números (para otras placas).
                elif len(re.findall(r'[A-Z]', texto_limpio)) >= 2 and len(re.findall(r'\d', texto_limpio)) >= 2:
                    candidatos.append((texto_limpio, altura, confianza))

        # Si no se encontró texto útil.
        if not candidatos:
            print("⚠️ OCR no encontró texto útil.")
            return ""

        # Ordenar por confianza primero.
        candidatos = sorted(candidatos, key=lambda x: x[2], reverse=True)

        # Seleccionar el texto con mejor confianza
        texto_final = candidatos[0][0]
        print("✅ Seleccionado:", texto_final)
        return texto_final

    except Exception as e:
        print("❌ Error OCR con EasyOCR:", e)
        return ""









