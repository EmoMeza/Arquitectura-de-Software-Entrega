from services import messageSender as ms

def switch(opcion, mensaje):
    if opcion == "1":
        print("Has seleccionado la opción 1 GRPC")
        ms.sendGRPC(mensaje)
    elif opcion == "2":
        print("Has seleccionado la opción 2 REST")
        ms.sendREST(mensaje)
    elif opcion == "3":
        print("Has seleccionado la opción 3 RabbitMQ")
        ms.sendRabbitMQ(mensaje)
    else:
        print("Opción inválida")

mensaje = input("Introduce un mensaje: ")
opcion = input("Selecciona el tipo de mensajero (1, 2 o 3):\n1= GRPC\n2= REST\n3= RabbitMQ\n")
switch(opcion, mensaje)