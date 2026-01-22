const input = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const messages = document.getElementById("messages");

let isThinking = false;

/* ===== Utils ===== */

function addMessage(type) {
    const msg = document.createElement("div");
    msg.className = `message ${type}`;
    const bubble = document.createElement("div");
    bubble.className = "bubble";
    msg.appendChild(bubble);
    messages.appendChild(msg);
    messages.scrollTop = messages.scrollHeight;
    return bubble;
}

function lockInput(state) {
    isThinking = state;
    input.disabled = state;
    sendBtn.disabled = state;
    input.placeholder = state
        ? "Phantom AI réfléchit..."
        : "Envoyer un message...";
}

/* ===== Typing Effect ===== */

function typeText(element, text, speed = 18) {
    return new Promise(resolve => {
        let i = 0;
        const interval = setInterval(() => {
            element.textContent += text.charAt(i);
            i++;
            messages.scrollTop = messages.scrollHeight;
            if (i >= text.length) {
                clearInterval(interval);
                resolve();
            }
        }, speed);
    });
}

/* ===== Main Send ===== */

async function sendMessage() {
    if (!input.value.trim() || isThinking) return;

    const userText = input.value.trim();
    input.value = "";

    // USER MESSAGE
    const userBubble = addMessage("user");
    userBubble.textContent = userText;

    // AI MESSAGE (EMPTY BUBBLE)
    const aiBubble = addMessage("ai");

    lockInput(true);

    try {
        const res = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userText })
        });

        const data = await res.json();

        // Typing animation
        await typeText(aiBubble, data.reply);

    } catch (err) {
        aiBubble.textContent = "❌ Erreur serveur.";
    }

    lockInput(false);
}

/* ===== Events ===== */

sendBtn.onclick = sendMessage;

input.addEventListener("keydown", e => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});
