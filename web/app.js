const input = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const messages = document.getElementById("messages");

function addMessage(text, type) {
    const msg = document.createElement("div");
    msg.className = `message ${type}`;
    msg.innerHTML = `<div class="bubble">${text}</div>`;
    messages.appendChild(msg);
    messages.scrollTop = messages.scrollHeight;
}

async function sendMessage() {
    if (!input.value.trim()) return;

    const userText = input.value;
    input.value = "";

    addMessage(userText, "user");
    addMessage("⏳ Phantom AI réfléchit…", "ai");

    const res = await fetch("/api/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: userText})
    });

    const data = await res.json();

    messages.lastChild.remove();
    addMessage(data.reply, "ai");
}

sendBtn.onclick = sendMessage;
input.addEventListener("keydown", e => {
    if (e.key === "Enter") sendMessage();
});
