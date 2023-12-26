# Proyecto de Comparación de Imágenes Faciales

Este proyecto utiliza la biblioteca `face_recognition` en Python para comparar dos imágenes faciales y determinar si pertenecen a la misma persona. Además, integra `pytesseract` para el reconocimiento óptico de caracteres (OCR), permitiendo extraer texto de imágenes, como datos de un DNI. Se ha añadido el uso de `labelImg` para el procesamiento de imágenes, facilitando la preparación de datos para entrenamiento de modelos. También, se integra YOLOv5 para la detección de objetos en imágenes.

## Características

- Comparación facial utilizando `face_recognition`.
- Extracción de texto de imágenes de DNI con `pytesseract`.
- Anotación de imágenes para el tratamiento de modelos con `labelImg`.
- Detección de objetos utilizando YOLOv5.
- API Flask para recibir imágenes y procesar las solicitudes.

## Requisitos Previos

- Python 3.8 o superior.
- CMake.
- Visual Studio con herramientas de desarrollo en C++.
- Tesseract OCR.
- PyQt5 (para `labelImg`).

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

6. **Instalar labelImg:**

- Instala las dependencias necesarias:

  - `$ pip install pyqt5 lxml`

- Luego instala labelImg:

  - `$ pip install labelImg`

7. **Integración con YOLOv5:**
   Para obtener más información sobre YOLOv5 y cómo usarlo en tu proyecto, visita [YOLOv5 GitHub Repository](https://github.com/ultralytics/yolov5).

**Nota:** Para la instalación en Windows, sigue este [tutorial de instalación](https://www.datasmarts.net/como-instalar-tesseract-ocr/) de Tesseract OCR.

## Configuración

1. **Clonar el repositorio:**

`$ git clone https://github.com/gastons-qwantec/comparar-dos-imagenes-demo`

2. **Instalar dependencias:**
   Navega al directorio del proyecto y ejecuta:

`$ pip install -r requirements.txt`

## Dockerización

Este proyecto puede ser ejecutado en contenedores Docker. Aquí te mostramos cómo configurarlo y ejecutarlo:

1. **Construye la imagen Docker:**

   `$ docker build -t nombre-de-tu-imagen .`

2. **Ejecuta tu aplicación en un contenedor Docker:**

   `$ docker run -p 5000:5000 nombre-de-tu-imagen`

## Uso

1. **Enviar solicitudes a la API:**
   Utiliza herramientas como Postman o escribe scripts en Python para enviar solicitudes POST con imágenes a `http://localhost:5000/process-dni`.

2. **Anotar imágenes con labelImg:**
   Ejecuta `labelImg` para abrir la interfaz.
   Selecciona y etiqueta las regiones de interés en tus imágenes con el comando en la terminal: `labelImg`

3. **Probar con imágenes:**
   Coloca las imágenes que deseas comparar en una carpeta y utiliza los endpoints de la API para procesarlas.

## Ejemplos

- Ejemplo de cómo comparar una foto de DNI y una foto personal para verificar la identidad.
- Ejemplo de cómo validar resultados con imágenes de diferentes personas.
