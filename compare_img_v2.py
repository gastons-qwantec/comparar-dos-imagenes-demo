import face_recognition
import numpy as np
import pytesseract
from PIL import Image


def process_dni_images(dni_image, user_image):
    # OCR para extraer texto del DNI
    # se require un tamaño de imagen estandar del DNI para que las cordenadas de la imagen coincidan siempre
    # standard_size = (1345, 851)
    # dni_image_original = Image.open("images/dni2.jpg")
    # dni_image_original = Image.open("images/dni.png") #no funciona porque es muy chica y al hacerla mas grande se pierde full calidad de elegibidad de la imagen (313x198)
    # dni_image = dni_image_original.resize(standard_size, Image.Resampling.LANCZOS)

    # Convertir imágenes PIL a arrays de NumPy
    # Convertir a RGB si la imagen está en un formato no compatible
    if dni_image.mode in ("RGBA", "P"):
        dni_image = dni_image.convert("RGB")
    if user_image.mode in ("RGBA", "P"):
        user_image = user_image.convert("RGB")
    user_image_np = np.array(user_image)

    # Coordenadas para el RUN
    x1_run, y1_run, x2_run, y2_run = 148, 730, 438, 778
    roi_run = dni_image.crop((x1_run, y1_run, x2_run, y2_run))

    # Coordenadas para los Apellidos
    x1_apellidos, y1_apellidos, x2_apellidos, y2_apellidos = 459, 141, 926, 233
    roi_apellidos = dni_image.crop(
        (x1_apellidos, y1_apellidos, x2_apellidos, y2_apellidos)
    )

    # Coordenadas para los Nombres
    x1_nombres, y1_nombres, x2_nombres, y2_nombres = 466, 264, 964, 308
    roi_nombres = dni_image.crop((x1_nombres, y1_nombres, x2_nombres, y2_nombres))

    # Coordenadas para el Número de Documento
    (
        x1_numero_documento,
        y1_numero_documento,
        x2_numero_documento,
        y2_numero_documento,
    ) = (
        775,
        422,
        1093,
        472,
    )
    roi_numero_documento = dni_image.crop(
        (
            x1_numero_documento,
            y1_numero_documento,
            x2_numero_documento,
            y2_numero_documento,
        )
    )

    # Extraer texto de cada ROI usando pytesseract
    text_run = pytesseract.image_to_string(roi_run, lang="spa")
    text_apellidos = pytesseract.image_to_string(roi_apellidos, lang="spa")
    text_nombres = pytesseract.image_to_string(roi_nombres, lang="spa")
    text_numero_documento = pytesseract.image_to_string(
        roi_numero_documento, lang="spa"
    )

    # Imprimir los resultados
    print("RUN:", text_run.strip())
    print("Apellidos:", text_apellidos.strip())
    print("Nombres:", text_nombres.strip())
    print("Número de Documento:", text_numero_documento.strip())

    # Coordenadas para la foto en el DNI
    x1_foto, y1_foto, x2_foto, y2_foto = 19, 249, 468, 670
    roi_foto_dni_np = np.array(dni_image.crop((x1_foto, y1_foto, x2_foto, y2_foto)))
    foto_dni_encoding = face_recognition.face_encodings(roi_foto_dni_np)[0]
    image2_encoding = face_recognition.face_encodings(user_image_np)[0]

    # Obtener la distancia entre las dos codificaciones
    # Mientras menor la distancia mayor la similitud, sirve para medir un nivel de confianza en la coincidencia
    face_distance = face_recognition.face_distance(
        [foto_dni_encoding], image2_encoding
    )[0]
    print("Distancia entre las caras:", face_distance)

    # Comparar las dos imágenes
    comparison_result = face_recognition.compare_faces(
        [foto_dni_encoding], image2_encoding
    )
    are_same_person = bool(comparison_result[0])

    print("¿Son la misma persona?:", are_same_person)

    if not are_same_person:
        # Las imágenes no son de la misma persona
        return {
            "Distancia entre las caras": face_distance,
            "¿Son la misma persona?": are_same_person,
        }

    return {
        "RUN": text_run.strip(),
        "Apellidos": text_apellidos.strip(),
        "Nombres": text_nombres.strip(),
        "Número de Documento": text_numero_documento.strip(),
        "Distancia entre las caras": face_distance,
        "¿Son la misma persona?": are_same_person,
    }
