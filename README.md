# Proyecto de Comparación de Imágenes Faciales

Este proyecto utiliza la biblioteca `face_recognition` en Python para comparar dos imágenes faciales y determinar si pertenecen a la misma persona.

## Requisitos Previos

- Python 3.8
- CMake
- Visual Studio

## Instalación

1. Instalar CMake.
2. Instalar Visual Studio con herramientas de desarrollo en C++.
3. Instalar `face_recognition`:
   `$ pip install face-recognition`

## Generación del `requirements.txt`

Para replicar el entorno en otra máquina, genera un archivo `requirements.txt` usando:

`pip freeze > requirements.txt`

Luego, instala las dependencias en otro entorno con:

`pip install -r requirements.txt`

## Uso

1. Coloca las imágenes que deseas comparar en una carpeta, por ejemplo, `images/`.
2. Ejecuta el script de Python que compara las imágenes.

## Ejemplos

- Comparación de una foto de DNI y una foto personal para verificar la identidad.
- Validación de resultados con imágenes de diferentes personas.
