import grpc
import services.message_pb2 as message_pb2
import services.message_pb2_grpc as message_pb2_grpc
import requests

def sendREST(mensaje):
        response = requests.post('http://localhost:5000/message', json={"texto": mensaje})
        print("Server response:", response.text)
        response = requests.get('http://localhost:6000/output')
        print("Websocket response:", response.text)
def sendRabbitMQ(mensaje):
        response = requests.post('http://localhost:5010/message', json={"texto": mensaje})
        print("Server response:", response.text)
        response = requests.get('http://localhost:6000/output')
        print("Websocket response:", response.text)
def sendGRPC(mensaje):
        with grpc.insecure_channel('localhost:5021') as channel:
                    stub = message_pb2_grpc.MessageServiceStub(channel)
                    response = stub.AddMessage(message_pb2.MessageRequest(message=mensaje))
                    print("Server response:", response.result)
        response = requests.get('http://localhost:6000/output')
        print("Websocket response:", response.text)