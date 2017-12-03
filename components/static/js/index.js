var web_socket_url = "ws://localhost:8001/";

$(document).ready(function() {
  var ws = new WebSocket(web_socket_url);
  console.log("testing");

  ws.onmessage = function(event) {
    //logic to process incoming push messages
    //goes here

  }
});
