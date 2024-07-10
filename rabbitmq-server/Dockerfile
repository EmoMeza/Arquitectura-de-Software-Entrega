# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY rabbitmq_server.py /app

# Instala Flask y pymongo
RUN pip install flask pymongo pika retry

# Expone el puerto en el que la aplicación correrá
EXPOSE 5010

# Comando para ejecutar la aplicación
CMD ["python", "rabbitmq_server.py"]
