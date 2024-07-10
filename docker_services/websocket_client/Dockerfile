# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY websocket_client.py /app

# Instala Flask y pymongo
RUN pip install flask_socketio requests websocket-client

# Expone el puerto en el que la aplicación correrá
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "websocket_client.py"]
