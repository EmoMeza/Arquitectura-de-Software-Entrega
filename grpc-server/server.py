# servidor_grpc.py
from concurrent import futures
import grpc
import psycopg2
from protos import my_service_pb2_grpc, my_service_pb2

class MyServiceServicer(my_service_pb2_grpc.MyServiceServicer):
    def MyMethod(self, request, context):
        message = request.message
        # Almacenar en la base de datos
        conn = psycopg2.connect(dbname="mi_base_de_datos", user="usuario", password="contraseña", host="db")
        cur = conn.cursor()
        cur.execute("INSERT INTO messages (message) VALUES (%s)", (message,))
        conn.commit()
        cur.close()
        conn.close()
        # Notificar al cliente WebSocket
        # Implementar la lógica de notificación
        return my_service_pb2.MyResponse(status="Mensaje recibido")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    my_service_pb2_grpc.add_MyServiceServicer_to_server(MyServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
