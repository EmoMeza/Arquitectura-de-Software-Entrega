const amqp = require("amqplib/callback_api");
const { MongoClient } = require("mongodb");
const WebSocket = require("ws");

const RABBITMQ_URL = "amqp://rabbitmq-server:5672";
const MONGO_URL = "mongodb://mongodb:27017";
const WEBSOCKET_URL = "ws://websocket-server:8080";
const DATABASE_NAME = "messages_db";
const COLLECTION_NAME = "messages";

MongoClient.connect(
  MONGO_URL,
  { useNewUrlParser: true, useUnifiedTopology: true },
  (err, client) => {
    if (err) throw err;

    const db = client.db(DATABASE_NAME);
    const collection = db.collection(COLLECTION_NAME);

    amqp.connect(RABBITMQ_URL, (error0, connection) => {
      if (error0) {
        throw error0;
      }

      connection.createChannel((error1, channel) => {
        if (error1) {
          throw error1;
        }

        const queue = "test_queue";

        channel.assertQueue(queue, {
          durable: false,
        });

        console.log(
          " [*] Waiting for messages in %s. To exit press CTRL+C",
          queue
        );

        channel.consume(
          queue,
          async (msg) => {
            const messageObject = JSON.parse(msg.content.toString());

            await collection.insertOne(messageObject);

            const totalMessages = await collection.countDocuments();

            const ws = new WebSocket(WEBSOCKET_URL);
            ws.on("open", () => {
              const notificationMessage = `Se ingresó un registro mediante ${messageObject.system}, con el mensaje ${messageObject.message}, total de mensajes ${totalMessages}`;
              ws.send(notificationMessage);
              ws.close();
            });

            console.log(" [x] Received %s", messageObject.message);
          },
          {
            noAck: true,
          }
        );
      });
    });
  }
);
