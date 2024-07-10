# Trabajo Semestral Arquitectura de Software

## Descripción

Este proyecto tiene como objetivo desarrollar un sistema de entrega de arquitectura de software utilizando Docker. La arquitectura se basa en microservicios, cada uno desplegado en un contenedor Docker, que se comunican entre sí para proporcionar diferentes funcionalidades. La arquitectura incluye servidores GRPC, REST, RabbitMQ, una base de datos y clientes para cada uno de estos servicios, así como un cliente WebSocket.

## Requisitos Previos

Para utilizar este proyecto, necesitas tener las siguientes herramientas instaladas:
- Docker
- Docker Compose

## Instalación

Para utilizar este proyecto, sigue estos pasos:

1. Clona el repositorio: 
    ```bash
    git clone https://github.com/EmoMeza/Arquitectura-de-Software-Entrega.git
    ```
2. Navega al directorio del proyecto:
    ```bash
    cd Arquitectura-de-Software-Entrega
    ```
3. Construye los contenedores y levanta los servicios:
    ```bash
    docker-compose up --build
    ```
4. Ejecuta el proyecto en segundo plano:
    ```bash
    docker-compose up -d
    ```

## Estructura del Proyecto

El proyecto está estructurado de la siguiente manera:

- **Base de Datos:**
  - Dockerfile para configurar y ejecutar la base de datos con persistencia de datos.

- **Servidor GRPC:**
  - Implementación de un servidor GRPC que recibe mensajes y los almacena en la base de datos.
  - Dockerfile para construir y ejecutar el servidor.

- **Servidor REST:**
  - Implementación de un servidor REST que recibe mensajes y los almacena en la base de datos.
  - Dockerfile para construir y ejecutar el servidor.

- **Servidor RabbitMQ:**
  - Configuración de un servidor RabbitMQ para la gestión de colas de mensajes.
  - Dockerfile para construir y ejecutar el servidor.

- **Clientes GRPC, REST, RabbitMQ y WebSocket:**
  - Implementación de clientes para interactuar con los respectivos servidores.
  - Dockerfiles para construir y ejecutar cada cliente.

- **Docker Compose:**
  - Archivo `docker-compose.yml` que define y configura todos los servicios y clientes, asegurando que estén en la misma red y que la base de datos tenga almacenamiento persistente.

## Configuración de Red

Todos los contenedores están configurados para estar en la misma red Docker personalizada para facilitar la comunicación.

## Interacción entre Contenedores

Cada vez que un cliente realiza una solicitud a un servidor, el mensaje se almacena en la base de datos. Al almacenar un mensaje en la base de datos, cualquier servidor envía una notificación al cliente WebSocket con el siguiente formato:
```json
"Se ingresó un registro mediante {tipocliente} , con el mensaje {mensaje}, total de mensajes {total}"
