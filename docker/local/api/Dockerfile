# Usa una imagen base de Python
FROM python:3.12-alpine

# set folder
WORKDIR /app

# copy requirements.txt
COPY requirements.txt /app/requirements.txt

# install requirements.txt
RUN pip install -U pip
RUN pip install -r /app/requirements.txt

# copy source code
COPY src /app/src

# Copy script for running
COPY /docker/local/api/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start