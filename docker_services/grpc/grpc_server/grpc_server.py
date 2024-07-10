from concurrent import futures
import grpc
import message_pb2
import message_pb2_grpc
from pymongo import MongoClient
from mongoengine import connect, Document, StringField, errors
import os
from datetime import datetime
from flask import Flask
from flask_socketio import SocketIO, emit
import threading

mongo_uri = os.environ.get('MONGO_URI', 'mongodb://root:example@localhost:27017')
client = MongoClient(mongo_uri)
db = client['messages']
collection = db['list']

app = Flask(__name__)
socketio = SocketIO(app)

# MongoDB Message Document
class Message(Document):
    content = StringField(required=True)

# gRPC Service Implementation
class MessageServiceServicer(message_pb2_grpc.MessageServiceServicer):
    def AddMessage(self, request, context):
        try:
            if not request.message:
                return message_pb2.MessageResponse(result='No message provided')

            message = Message(content=request.message)
            data = {
                'Texto': message.content,
                'FechaHora': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'Sistema': "GRPC",
                'Estado': 0
            }
            collection.insert_one(data)

            # Emitting WebSocket message
            total_messages = collection.count_documents({})
            socketio.emit('message_uploaded', {
                'message': f"Se ingresó un registro mediante GRPC, con el mensaje \"{message.content}\", total de mensajes {total_messages}"
            })

            return message_pb2.MessageResponse(result=f'Texto:{message.content}, FechaHora:{data["FechaHora"]}, Sistema:{data["Sistema"]}, Estado:{data["Estado"]} ')
        except Exception as e:
            print(f"Failed to save message: {e}")
            return message_pb2.MessageResponse(result='Failed to save message due to internal error')

def grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    message_pb2_grpc.add_MessageServiceServicer_to_server(MessageServiceServicer(), server)
    server.add_insecure_port('[::]:5020')
    server.start()
    server.wait_for_termination()

# Running Flask-SocketIO alongside gRPC server in a separate thread
if __name__ == '__main__':
    print("Starting gRPC server thread...")
    grpc_thread = threading.Thread(target=grpc_server)
    grpc_thread.start()
    print("Starting Flask-SocketIO server...")
    socketio.run(app, host='0.0.0.0', port=5031, allow_unsafe_werkzeug=True)
