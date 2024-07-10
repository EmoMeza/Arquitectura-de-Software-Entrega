import socketio
import os
import threading

def start_websocket_client(url):
    print("Starting WebSocket client...", flush=True)
    # Initialize SocketIO client
    sio = socketio.Client()

    # Define event handler for 'message_uploaded'
    @sio.event
    def message_uploaded(data):
        print(f"{data['message']}", flush=True)

    # Connect to the server
    sio.connect(url)

    # Main loop to keep the connection open
    try:
        sio.wait()
    except KeyboardInterrupt:
        print("Client terminated by user.", flush=True)
        sio.disconnect()

#create the main function
if __name__ == "__main__":
    url1 = os.environ.get('REST_SERVER_URL', 'http://localhost:5000')
    url2 = os.environ.get('RABBITMQ_SERVER_URL', 'http://localhost:5010')
    url3 = os.environ.get('GRPC_SERVER_URL', 'http://localhost:5030')


    # Create threads for each URL
    thread1 = threading.Thread(target=start_websocket_client, args=(url1,))
    thread2 = threading.Thread(target=start_websocket_client, args=(url2,))
    thread3 = threading.Thread(target=start_websocket_client, args=(url3,))

    # Start the threads
    thread1.start()
    thread2.start()
    thread3.start()

    # Wait for the threads to finish
    thread1.join()
    thread2.join()
    thread3.join()
