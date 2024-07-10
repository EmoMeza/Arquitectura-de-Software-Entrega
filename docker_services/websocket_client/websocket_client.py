import socketio
import os
import threading
import sys
from flask import Flask, request, jsonify

app = Flask(__name__)
sys.stdout = open('output.log', 'w')

def start_websocket_client(url):
    print("Starting WebSocket client...", flush=True)
    sio = socketio.Client()

    @sio.event
    def message_uploaded(data):
        print(f"{data['message']}", flush=True)

    sio.connect(url)

    try:
        sio.wait()
    except KeyboardInterrupt:
        print("Client terminated by user.", flush=True)
        sio.disconnect()

def start_threads():
    urls = [
        os.environ.get('REST_SERVER_URL', 'http://localhost:5000'),
        os.environ.get('RABBITMQ_SERVER_URL', 'http://localhost:5010'),
        os.environ.get('GRPC_SERVER_URL', 'http://localhost:5031')
    ]

    threads=[]
    for url in urls:
        thread = threading.Thread(target=start_websocket_client, args=(url,))
        thread.start()
        threads.append(thread)

@app.route('/output', methods=['GET'])
def get_output():
    with open('output.log', 'r') as f:
        lines = f.readlines()
        last_line = lines[-1] if lines else ""
        return last_line

if __name__ == '__main__':
    start_threads()
    app.run(host='0.0.0.0', port=6000)