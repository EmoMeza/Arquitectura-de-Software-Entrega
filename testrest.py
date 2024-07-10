# test_client.py

import requests
import json
from datetime import datetime

# URL of the client service running inside Docker
url = 'http://localhost:5001/send_message'

# Data to send to the client service
data = {
    "texto": "No hay nada más noble que hacer el bien sin esperar nada a cambio",
}

# Convert data to JSON
json_data = json.dumps(data)

# Send a POST request to the client service
response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'})

# Print the response from the client service
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
