# Usa una imagen base de Python
FROM python:3.9-slim
WORKDIR /app
COPY grpc_server.py /app
RUN pip install grpcio grpcio-tools pymongo
CMD ["python", "grpc_server.py"]
