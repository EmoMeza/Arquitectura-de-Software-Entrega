const WebSocket = require("ws");
const ws = new WebSocket("ws://websocket-server:8080");

ws.on("open", function open() {
  console.log("WebSocket client connected");
  ws.send("Hello WebSocket Server");
});

ws.on("message", function incoming(data) {
  console.log("WebSocket client received: %s", data);
});
