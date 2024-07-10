
import grpc
import requests
from services import GRPC_Sender
def get_last_line():
    pass
def switch(opcion, mensaje):
    if opcion == "1":
        print("Has seleccionado la opción 1 GRPC")
        GRPC_Sender.SendGRPC(mensaje)
        response = requests.get('http://localhost:6000/output')
        print("Websocket response:", response.text)
    elif opcion == "2":
        print("Has seleccionado la opción 2 REST")
        response = requests.post('http://localhost:5000/message', json={"texto": mensaje})
        print("Server response:", response.text)
        response = requests.get('http://localhost:6000/output')
        print("Websocket response:", response.text)
    elif opcion == "3":
        print("Has seleccionado la opción 3 RabbitMQ")
        response = requests.post('http://localhost:5010/message', json={"texto": mensaje})
        print("Server response:", response.text)
        response = requests.get('http://localhost:6000/output')
        print("Websocket response:", response.text)
    else:
        print("Opción inválida")


mensaje = input("Introduce un mensaje: ")
opcion = input("Selecciona el tipo de mensajero (1, 2 o 3):\n1= GRPC\n2= REST\n3= RabbitMQ\n")
switch(opcion, mensaje)
