from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import os
import json  # Add this import
from datetime import datetime
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)
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
def create_message():
    json_data = request.get_json()
    data = {
        'Texto': json_data['texto'],
        'FechaHora': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'Sistema': "REST",
        'Estado': 0
    }
    result = collection.insert_one(data)
    data['_id'] = str(result.inserted_id)  # Convert ObjectId to string
    response = {
        "status": "success",
        "data": data
    }

        # Emitting WebSocket message
    total_messages = collection.count_documents({})
    message = {
        'clientType': data['Sistema'],
        'content': json_data['texto']
    }
    socketio.emit('message_uploaded', {
        'message': f"Se ingresó un registro mediante {message['clientType']}, con el mensaje \"{message['content']}\", total de mensajes {total_messages}"
    })
    return app.response_class(
        response=json.dumps(response, cls=JSONEncoder),
        status=201,
        mimetype='application/json'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5040)
