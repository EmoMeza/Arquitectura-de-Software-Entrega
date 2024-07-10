const WebSocket = require("ws");
const wss = new WebSocket.Server({ port: 8080 });

wss.on("connection", function connection(ws) {
  console.log("WebSocket server connected");
  ws.send("WebSocket server says hello");
});

module.exports = wss;
