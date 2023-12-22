# Proyecto de Comparación de Imágenes Faciales

Este proyecto utiliza la biblioteca `face_recognition` en Python para comparar dos imágenes faciales y determinar si pertenecen a la misma persona. Además, integra `pytesseract` para el reconocimiento óptico de caracteres (OCR), permitiendo extraer texto de imágenes, como datos de un DNI.

## Características

- Comparación facial utilizando `face_recognition`.
- Extracción de texto de imágenes de DNI con `pytesseract`.
- API Flask para recibir imágenes y procesar las solicitudes.

## Requisitos Previos

- Python 3.8 o superior.
- CMake.
- Visual Studio con herramientas de desarrollo en C++.
- Tesseract OCR.

## Instalación

1. **Instalar CMake:**
   Descargar e instalar desde [CMake Official Website](https://cmake.org/download/).

2. **Instalar Visual Studio:**
   Asegúrate de incluir las herramientas de desarrollo en C++ durante la instalación. [Visual Studio](https://visualstudio.microsoft.com/downloads/).

3. **Instalar face_recognition:**

   `$ pip install face-recognition`

4. **Instalar Tesseract OCR:**
   Descargar e instalar desde [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).

5. **Instalar pytesseract:**

**Nota:** Para la instalación en Windows, sigue este [tutorial de instalación](https://www.datasmarts.net/como-instalar-tesseract-ocr/).

## Configuración

1. **Clonar el repositorio:**

`$git clone https://github.com/gastons-qwantec/comparar-dos-imagenes-demo`

2. **Instalar dependencias:**
   Navega al directorio del proyecto y ejecuta:

`$ pip install -r requirements.txt`

## Uso

1. **Ejecutar el servidor Flask:**

Esto iniciará el servidor en `localhost` en el puerto `5000`.

2. **Enviar solicitudes a la API:**
   Utiliza herramientas como Postman o escribe scripts en Python para enviar solicitudes POST con imágenes a `http://localhost:5000/process-dni`.

3. **Probar con imágenes:**
   Coloca las imágenes que deseas comparar en una carpeta y utiliza los endpoints de la API para procesarlas.

## Ejemplos

- Ejemplo de cómo comparar una foto de DNI y una foto personal para verificar la identidad.
- Ejemplo de cómo validar resultados con imágenes de diferentes personas.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, lee `CONTRIBUTING.md` para obtener detalles sobre nuestro código de conducta y el proceso para enviarnos pull requests.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo `LICENSE` para más detalles.
