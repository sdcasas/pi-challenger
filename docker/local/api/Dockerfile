# Usa una imagen base de Python
FROM python:3.12-alpine

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt /app/requirements.txt

# Instala las dependencias del proyecto
RUN pip install -U pip
RUN pip install -r /app/requirements.txt

# Copia el resto del código al contenedor
COPY /src /app

# Expón el puerto en el que se ejecutará la aplicación
EXPOSE 8000

WORKDIR /app/src

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
