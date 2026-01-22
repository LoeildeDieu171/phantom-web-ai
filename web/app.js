const input = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const messages = document.getElementById("messages");

let locked = false;

/* CREATE MESSAGE */
function createBubble(type) {
    const msg = document.createElement("div");
    msg.className = `message ${type}`;

    const bubble = document.createElement("div");
    bubble.className = "bubble";

    msg.appendChild(bubble);
    messages.appendChild(msg);
    messages.scrollTop = messages.scrollHeight;

    return bubble;
}

/* LOCK INPUT */
function lock(state) {
    locked = state;
    input.disabled = state;
    sendBtn.disabled = state;
    input.placeholder = state
        ? "Phantom AI écrit..."
        : "Envoyer un message...";
}

/* TYPING EFFECT */
function typeWriter(element, text, speed = 16) {
    element.textContent = "";
    let i = 0;

    const interval = setInterval(() => {
        element.textContent += text.charAt(i);
        i++;
        messages.scrollTop = messages.scrollHeight;

        if (i >= text.length) clearInterval(interval);
    }, speed);
}

/* SEND MESSAGE */
async function sendMessage() {
    if (!input.value.trim() || locked) return;

    const userText = input.value;
    input.value = "";

    createBubble("user").textContent = userText;
    const aiBubble = createBubble("ai");

    lock(true);

    try {
        const res = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userText })
        });

        const data = await res.json();
        typeWriter(aiBubble, data.reply);

    } catch {
        aiBubble.textContent = "Erreur serveur.";
    }

    setTimeout(() => lock(false), 300);
}

/* EVENTS */
sendBtn.onclick = sendMessage;

input.addEventListener("keydown", e => {
    if (e.key === "Enter") {
        e.preventDefault();
        sendMessage();
    }
});
