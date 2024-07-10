import pika
import os
import json
from pymongo import MongoClient
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import os
import json  # Add this import
from datetime import datetime

##MONOGO

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


##RABBITMQ
def create_channel():
    rabbit_conn = os.environ.get('RABBITMQ', 'localhost')
    # Establish a connection to RabbitMQ server running locally (replace with your RabbitMQ server details if remote)
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_conn))
    channel = connection.channel()
    channel.queue_declare(queue='test')
    return channel

def send_messageRabbitMQ(message):
    # Create a channel
    # Declare a queue named 'hello' to which the message will be sent
    # Send a message to the queue
    channel = create_channel()
    channel.basic_publish(exchange='',
                        routing_key='test',
                        body=message)
    print(f" [x] Sent '{message}'")
    # Close the connection to RabbitMQ server


@app.route('/message', methods=['POST'])
def create_message():
    json_data = request.get_json()
    send_messageRabbitMQ(json_data['texto'])
    data = {
        'Texto': json_data['texto'],
        'FechaHora': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'Sistema': "RabbitMQ",
        'Estado': 0
    }
    result = collection.insert_one(data)
    data['_id'] = str(result.inserted_id)  # Convert ObjectId to string
    response = {
        "status": "success",
        "data": data
    }
    return app.response_class(
        response=json.dumps(response, cls=JSONEncoder),
        status=201,
        mimetype='application/json'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010)

