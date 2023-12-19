import face_recognition

# carga de la primera imagen en este caso la dni a comprar.
image1 = face_recognition.load_image_file("images/dni.png")
image1_encoding = face_recognition.face_encodings(image1)[0]

# Cargar la segunda imagen de una persona tomada de la camara de perfil.

image2 = face_recognition.load_image_file("images/real.png")
# image2 = face_recognition.load_image_file("images/rey.jpg")
image2_encoding = face_recognition.face_encodings(image2)[0]

# Comparar las dos imágenes
results = face_recognition.compare_faces([image1_encoding], image2_encoding)
print("¿Son la misma persona?:", results[0])
