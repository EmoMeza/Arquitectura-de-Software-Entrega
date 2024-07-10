FROM python:3.9-slim
WORKDIR /app
COPY rest_client.py /app
RUN pip install flask requests
CMD ["python", "rest_client.py"]