import face_recognition
import numpy as np
import pytesseract
import torch
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

model = torch.hub.load("ultralytics/yolov5", "custom", path="models/dni_chile_model.pt")


def preprocess_image_for_ocr(image):
    # Aplicar filtros para mejorar la calidad de la imagen para OCR
    image = image.convert("L")  # Convertir a escala de grises
    image = image.filter(ImageFilter.MedianFilter())  # Filtro para reducir ruido
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)  # Mejorar el contraste
    image = image.filter(ImageFilter.SHARPEN)  # Afinar la imagen
    return image


def extract_text_from_image(image):
    processed_image = preprocess_image_for_ocr(image)
    return pytesseract.image_to_string(
        processed_image, lang="spa", config="--psm 6"
    ).strip()


def resize_image_keep_aspect(dni_image, target_size=640):
    # Calcular la nueva dimensión manteniendo la relación de aspecto
    aspect_ratio = dni_image.width / dni_image.height
    if aspect_ratio > 1:  # La imagen es más ancha que alta
        new_width = target_size
        new_height = int(target_size / aspect_ratio)
    else:  # La imagen es más alta que ancha
        new_height = target_size
        new_width = int(target_size * aspect_ratio)

    # Redimensionar la imagen
    resized_img = dni_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return resized_img


def process_dni_images(dni_image, user_image):
    # Convertir a RGB si la imagen está en un formato no compatible
    dni_image = convert_to_rgb_if_needed(dni_image)
    user_image = convert_to_rgb_if_needed(user_image)

    # Redimensionar la imagen para el modelo
    resized_image = resize_image_keep_aspect(dni_image)

    # Obtener resultados del modelo
    results = model(resized_image)

    # Inicializar el diccionario de resultados
    extracted_info = {}

    # Procesar cada detección
    for *xyxy, conf, cls in results.xyxy[0].numpy():
        label = results.names[int(cls)]
        if label == "DNI_TARJETA":
            # Omitir la etiqueta DNI_TARJETA
            continue

        bbox = [round(x) for x in xyxy]  # Coordenadas de la caja delimitadora
        if label == "DNI_FOTO":
            # Procesar para comparación facial
            face_distance, are_same_person = compare_faces(dni_image, user_image, bbox)
            extracted_info["distancia_cara"] = face_distance
            extracted_info["misma_persona"] = are_same_person
        else:
            # Procesar para extracción de texto con OCR
            roi = resized_image.crop(bbox)
            text = extract_text_from_image(roi)
            extracted_info[label] = text

    return extracted_info


def convert_to_rgb_if_needed(image):
    if image.mode in ("RGBA", "P"):
        return image.convert("RGB")
    return image


def compare_faces(dni_image, user_image, foto_coords):
    roi_foto_dni_np = np.array(dni_image.crop(foto_coords))
    encodings_dni = face_recognition.face_encodings(roi_foto_dni_np)

    if len(encodings_dni) == 0:
        # No se detectaron caras en la imagen del DNI
        return None, False

    foto_dni_encoding = encodings_dni[0]
    user_image_np = np.array(user_image)
    encodings_user = face_recognition.face_encodings(user_image_np)

    if len(encodings_user) == 0:
        # No se detectaron caras en la imagen del usuario
        return None, False

    image2_encoding = encodings_user[0]

    # Obtener la distancia entre las dos codificaciones
    face_distance = face_recognition.face_distance(
        [foto_dni_encoding], image2_encoding
    )[0]

    # Comparar las dos imágenes
    comparison_result = face_recognition.compare_faces(
        [foto_dni_encoding], image2_encoding
    )
    are_same_person = bool(comparison_result[0])

    return face_distance, are_same_person
