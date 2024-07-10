# servidor_grpc.py
from concurrent import futures
import grpc
from pymongo import MongoClient
from protos import grpc_service_pb2_grpc, grpc_service_pb2
from websocket import create_connection

class MyServiceServicer(grpc_service_pb2_grpc.MyServiceServicer):
    def __init__(self):
        self.client = MongoClient('mongodb://mongodb:27017/')
        self.db = self.client.my_database

    def MyMethod(self, request, context):
        message = request.message
        # Almacenar en la base de datos
        self.db.messages.insert_one({"message": message})
        
        # Notificar al cliente WebSocket
        ws = create_connection("ws://websocket-server:8080")
        ws.send(f"Se ingresó un registro mediante GRPC con el mensaje {message}")
        ws.close()
        
        return grpc_service_pb2.MyResponse(status="Mensaje recibido")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grpc_service_pb2_grpc.add_MyServiceServicer_to_server(MyServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()