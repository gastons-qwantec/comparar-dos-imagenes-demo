# Usa una imagen base oficial de Python
FROM python:3.8

# Establece el directorio de trabajo en el contenedor
WORKDIR /usr/src/app

# Copia el archivo de requisitos y lo instala
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código fuente de tu aplicación
COPY . .

# Comando para ejecutar la aplicación
CMD [ "python", "./app.py" ]
