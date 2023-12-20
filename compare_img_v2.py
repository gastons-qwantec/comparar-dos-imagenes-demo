import face_recognition
import numpy as np
import pytesseract
from PIL import Image

# OCR para extraer texto del DNI
dni_image = Image.open("images/dni2.jpg")
dni_text = pytesseract.image_to_string(dni_image, lang="spa")
# imprimiendo contenido
print(dni_text)

image1 = face_recognition.load_image_file("images/dni2.jpg")
image1_encoding = face_recognition.face_encodings(image1)[0]

# Cargar la segunda imagen de una persona tomada de la camara de perfil.

# image2 = face_recognition.load_image_file("images/real.png")
image2 = face_recognition.load_image_file("images/reyna.jpg")
# image2 = face_recognition.load_image_file("images/rey.jpg")
image2_encoding = face_recognition.face_encodings(image2)[0]

# Comparar las dos imágenes
results = face_recognition.compare_faces([image1_encoding], image2_encoding)
print("¿Son la misma persona?:", results[0])
