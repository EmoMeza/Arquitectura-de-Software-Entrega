const WebSocket = require('ws');
const mongoose = require('mongoose');

// Conectar a MongoDB
mongoose.connect('mongodb://root:example@mongodb:27017/mydatabase', { useNewUrlParser: true, useUnifiedTopology: true });

const MessageSchema = new mongoose.Schema({
  content: String,
  clientType: String
});

const Message = mongoose.model('Message', MessageSchema);

// Configurar WebSocket
const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', ws => {
  console.log('New client connected');

  // Enviar notificación cuando se inserte un nuevo mensaje
  ws.on('message', async data => {
    const message = JSON.parse(data);
    const newMessage = new Message({ content: message.content, clientType: message.clientType });
    await newMessage.save();

    const totalMessages = await Message.countDocuments();

    ws.send(`Se ingresó un registro mediante ${message.clientType}, con el mensaje ${message.content}, total de mensajes ${totalMessages}`);
  });
});