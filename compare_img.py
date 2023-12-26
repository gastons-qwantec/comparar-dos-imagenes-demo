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

    # Uso de la función
    resized_image = resize_image_keep_aspect(dni_image)
    resized_image.show()

    user_image = convert_to_rgb_if_needed(user_image)

    results = model(resized_image)

    # Imprimir los resultados
    print("Resultados:")
    print(results)
    results.print()

    # Coordenadas de las regiones de interés (ROI) en el DNI
    roi_coords = {
        "run": (155, 730, 438, 778),
        "apellidos": (459, 141, 860, 233),
        "nombres": (466, 264, 964, 308),
        "numero_documento": (775, 422, 1093, 472),
        "foto": (19, 249, 468, 670),
    }

    # Extraer texto de cada ROI usando pytesseract
    text_run = extract_text_from_image(dni_image.crop(roi_coords["run"]))
    text_apellidos = extract_text_from_image(dni_image.crop(roi_coords["apellidos"]))
    text_nombres = extract_text_from_image(dni_image.crop(roi_coords["nombres"]))
    text_numero_documento = extract_text_from_image(
        dni_image.crop(roi_coords["numero_documento"])
    )

    # Imprimir los resultados
    print("RUN:", text_run)
    print("Apellidos:", text_apellidos)
    print("Nombres:", text_nombres)
    print("Número de Documento:", text_numero_documento)

    # Comparación de rostros
    face_distance, are_same_person = compare_faces(
        dni_image, user_image, roi_coords["foto"]
    )

    if not are_same_person:
        return {
            "distancia_cara": face_distance,
            "misma_persona": are_same_person,
        }

    return {
        "RUN": text_run,
        "Apellidos": text_apellidos,
        "Nombres": text_nombres,
        "Nun_doc": text_numero_documento,
        "distancia_cara": face_distance,
        "misma_persona": are_same_person,
    }


def convert_to_rgb_if_needed(image):
    if image.mode in ("RGBA", "P"):
        return image.convert("RGB")
    return image


def compare_faces(dni_image, user_image, foto_coords):
    roi_foto_dni_np = np.array(dni_image.crop(foto_coords))
    foto_dni_encoding = face_recognition.face_encodings(roi_foto_dni_np)[0]
    user_image_np = np.array(user_image)
    image2_encoding = face_recognition.face_encodings(user_image_np)[0]

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
