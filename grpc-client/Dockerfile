FROM python:3.9-slim
WORKDIR /app
COPY grpc_client.py /app
RUN pip install grpcio grpcio-tools
CMD ["python", "grpc_client.py"]    