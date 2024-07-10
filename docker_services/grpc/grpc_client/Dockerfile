# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY grpc_client.py /app
COPY message.proto /app
COPY message_pb2.py /app
COPY message_pb2_grpc.py /app

# Instala Flask y pymongo
RUN pip install pymongo grpcio-tools grpcio mongoengine

# Expone el puerto en el que la aplicación correrá
EXPOSE 5021

# Comando para ejecutar la aplicación
CMD ["python", "grpc_client.py"]
