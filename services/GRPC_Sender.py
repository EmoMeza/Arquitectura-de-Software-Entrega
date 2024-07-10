import grpc
import services.message_pb2 as message_pb2
import services.message_pb2_grpc as message_pb2_grpc



def SendGRPC(mensaje):
    with grpc.insecure_channel('localhost:5021') as channel:
            stub = message_pb2_grpc.MessageServiceStub(channel)
            response = stub.AddMessage(message_pb2.MessageRequest(message=mensaje))
            print("Server response:", response.result)