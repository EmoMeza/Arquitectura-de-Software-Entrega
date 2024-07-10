FROM python:3.8-slim

WORKDIR /app

COPY rest_server.py /app

RUN pip install flask pymongo

EXPOSE 5000

CMD ["python", "rest_server.py"]
