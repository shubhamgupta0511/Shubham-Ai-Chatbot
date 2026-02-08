async function sendMessage(){

let input = document.getElementById("user-input");
let chatBox = document.getElementById("chat-box");

let userText = input.value.trim();
if(!userText) return;

// user bubble
chatBox.innerHTML += `<div class="message user">${userText}</div>`;
input.value="";
chatBox.scrollTop = chatBox.scrollHeight;

// typing animation
let typing = document.createElement("div");
typing.className="message bot";
typing.id="typing";
typing.innerHTML = `
<div class="typing">
<span></span><span></span><span></span>
</div>`;
chatBox.appendChild(typing);
chatBox.scrollTop = chatBox.scrollHeight;

// API call
let response = await fetch("/chat",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({message:userText})
});

let data = await response.json();

// remove typing
document.getElementById("typing").remove();

// bot reply
chatBox.innerHTML += `<div class="message bot">${data.reply}</div>`;
chatBox.scrollTop = chatBox.scrollHeight;
input.focus();
}

// enter key
document.getElementById("user-input").addEventListener("keypress",function(e){
if(e.key==="Enter"){
sendMessage();
}
});

function clearChat(){
document.getElementById("chat-box").innerHTML="";
}
