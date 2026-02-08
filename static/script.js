async function sendMessage() {
    let input = document.getElementById("user-input");
    let chatBox = document.getElementById("chat-box");

    let userText = input.value;
    if (!userText) return;

    // user message
    chatBox.innerHTML += `<div class="message user">${userText}</div>`;
    input.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

    // typing animation
    let typingDiv = document.createElement("div");
    typingDiv.className = "message bot";
    typingDiv.id = "typing";
    typingDiv.innerHTML = "Typing...";
    chatBox.appendChild(typingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

    // API call
    let response = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ message: userText })
    });

    let data = await response.json();

    // remove typing
    document.getElementById("typing").remove();

    // bot reply
    chatBox.innerHTML += `<div class="message bot">${data.reply}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
}


document.getElementById("user-input")
.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});
