const amqp = require('amqplib/callback_api');
const readline = require('readline');

// RabbitMQ connection string
const RABBITMQ_URL = 'amqp://localhost:5672';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.question('Enter the message to send: ', (msg) => {
  amqp.connect(RABBITMQ_URL, (error0, connection) => {
    if (error0) {
      throw error0;
    }

    connection.createChannel((error1, channel) => {
      if (error1) {
        throw error1;
      }

      const queue = 'test_queue';

      channel.assertQueue(queue, {
        durable: false
      });

      channel.sendToQueue(queue, Buffer.from(msg));
      console.log(` [x] Sent '${msg}'`);

      setTimeout(() => {
        connection.close();
        process.exit(0);
      }, 500);
    });
  });

  rl.close();
});
