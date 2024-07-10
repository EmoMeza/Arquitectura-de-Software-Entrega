import grpc
import grpc_service_pb2
import grpc_service_pb2_grpc

def run():
    with grpc.insecure_channel('grpc-server:50051') as channel:
        stub = grpc_service_pb2_grpc.MyServiceStub(channel)
        response = stub.MyMethod(grpc_service_pb2.MyRequest(message='Hello, GRPC Server!'))
        print("GRPC Client received: " + response.message)

if __name__ == '__main__':
    run()