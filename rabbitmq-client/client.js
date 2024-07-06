const amqp = require('amqplib');

async function sendMessage() {
  try {
    // Conectar a RabbitMQ
    const connection = await amqp.connect('amqp://localhost:15672');
    const channel = await connection.createChannel();
    
    // Declarar una cola
    const queue = 'test_queue';
    await channel.assertQueue(queue, {
      durable: false
    });

    // Enviar un mensaje
    const message = 'Hello, RabbitMQ!';
    channel.sendToQueue(queue, Buffer.from(message));
    console.log(`Sent: ${message}`);

    // Cerrar la conexión y el canal
    setTimeout(() => {
      channel.close();
      connection.close();
    }, 500);
  } catch (error) {
    console.error('Error:', error);
  }
}

sendMessage();
