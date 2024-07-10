# Dockerfile for Client Script

# Use a Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

COPY rest_client.py /app

# Install Flask and requests module
RUN pip install --no-cache-dir Flask requests

# Command to run the client script
CMD ["python", "rest_client.py"]
