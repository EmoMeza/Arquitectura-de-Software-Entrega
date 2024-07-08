from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import os
import json  # Add this import
from datetime import datetime

app = Flask(__name__)
# Conexión a MongoDB
mongo_uri = os.environ.get('MONGO_URI', 'mongodb://root:example@localhost:27017')
client = MongoClient(mongo_uri)
db = client['messages']
collection = db['list']

# Custom JSON encoder to handle ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super(JSONEncoder, self).default(o)

app.json_encoder = JSONEncoder

@app.route('/message', methods=['POST'])
def save_message():
    data = request.json
    if data:
        result = collection.insert_one(data)
        data['_id'] = str(result.inserted_id)
        return jsonify({"status": "success", "data": data}), 201
    return jsonify({"status": "error", "message": "No data provided"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
