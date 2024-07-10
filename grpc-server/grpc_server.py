from concurrent import futures
import grpc
import message_pb2
from datetime import datetime
import message_pb2_grpc
from pymongo import MongoClient
from mongoengine import connect, Document, StringField, errors
import os

mongo_uri = os.environ.get('MONGO_URI', 'mongodb://root:example@localhost:27017')
client = MongoClient(mongo_uri)
db = client['messages']
collection = db['list']

class Message(Document):
    content = StringField(required=True)

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
            print(data)
            return message_pb2.MessageResponse(result='Message added successfully')
        except errors.ValidationError as e:
            return message_pb2.MessageResponse(result=str(e))
        except errors.NotUniqueError:
            return message_pb2.MessageResponse(result='Message already exists')
        except Exception as e:
            print(f"Failed to save message: {e}")
            return message_pb2.MessageResponse(result='Failed to save message due to internal error')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    message_pb2_grpc.add_MessageServiceServicer_to_server(MessageServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
