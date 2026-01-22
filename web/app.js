const input = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const messages = document.getElementById("messages");

let locked = false;

function bubble(type) {
    const msg = document.createElement("div");
    msg.className = `message ${type}`;
    const b = document.createElement("div");
    b.className = "bubble";
    msg.appendChild(b);
    messages.appendChild(msg);
    messages.scrollTop = messages.scrollHeight;
    return b;
}

function type(el, text) {
    el.textContent = "";
    let i = 0;
    const t = setInterval(() => {
        el.textContent += text[i++];
        messages.scrollTop = messages.scrollHeight;
        if (i >= text.length) clearInterval(t);
    }, 15);
}

async function send() {
    if (locked || !input.value.trim()) return;

    locked = true;
    sendBtn.disabled = true;
    input.disabled = true;

    const text = input.value;
    input.value = "";

    bubble("user").textContent = text;
    const ai = bubble("ai");

    try {
        const r = await fetch("/api/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message: text})
        });

        const d = await r.json();
        type(ai, d.reply || "Réponse vide.");

    } catch (e) {
        type(ai, "Erreur JS : " + e.message);
    }

    setTimeout(() => {
        locked = false;
        sendBtn.disabled = false;
        input.disabled = false;
        input.focus();
    }, 300);
}

sendBtn.onclick = send;
input.addEventListener("keydown", e => {
    if (e.key === "Enter") send();
});
