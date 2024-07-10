from flask import Flask, request, jsonify
import requests
import json
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        url = os.environ.get('REST_SERVER_URL', 'http://localhost:5040') + "/message"  # Use the Docker service name 'flask-service'

        # Forward the received data to the Flask service
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        # Handle any request exceptions
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        # Handle any other exceptions
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
