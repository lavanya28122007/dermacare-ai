function sendMessage() {
  var msg = document.getElementById("message").value;

  if(msg.trim() == ""){
    return;
  }

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/chat", true);
  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhr.onload = function () {
    var reply = JSON.parse(this.responseText).reply;
    document.getElementById("chatbox").innerHTML += "<p class='user'>You: " + msg + "</p>";
    document.getElementById("chatbox").innerHTML += "<p class='bot'>Bot: " + reply + "</p>";
    document.getElementById("message").value = "";
    document.getElementById("chatbox").scrollTop = document.getElementById("chatbox").scrollHeight;
  };
  xhr.send("message=" + msg);
}
