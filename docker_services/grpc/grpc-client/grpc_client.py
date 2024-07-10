import grpc
import message_pb2
import message_pb2_grpc
from concurrent import futures
import grpc
import message_pb2
import message_pb2_grpc
from mongoengine import  Document, StringField
import os


inscure_channel_name = os.environ.get('INSECURE_CHANNEL_NAME', 'localhost') + ":5020" 


class Message(Document):
    content = StringField(required=True)

class MessageServiceServicer(message_pb2_grpc.MessageServiceServicer):
    def AddMessage(self, request, context):
        try:
            with grpc.insecure_channel(inscure_channel_name) as channel:
                stub = message_pb2_grpc.MessageServiceStub(channel)
                response = stub.AddMessage(message_pb2.MessageRequest(message= Message(content=request.message).content))
                print("Server response:", response.result)
                return response
        except Exception as e:
            print(f"Failed to save message: {e}")
            return message_pb2.MessageResponse(result='Failed to save message due to internal error')

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    message_pb2_grpc.add_MessageServiceServicer_to_server(MessageServiceServicer(), server)
    server.add_insecure_port('[::]:5021')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()