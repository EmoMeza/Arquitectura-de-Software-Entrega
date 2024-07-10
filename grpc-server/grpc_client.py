import grpc
import message_pb2
import message_pb2_grpc

def run():
    # Assuming the server is running on localhost:50051
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = message_pb2_grpc.MessageServiceStub(channel)
        response = stub.AddMessage(message_pb2.MessageRequest(message="Hello, world!"))
        print("Server response:", response.result)

if __name__ == "__main__":
    run()