const input = document.getElementById("input");
const sendBtn = document.getElementById("send");
const messages = document.getElementById("messages");

let locked = false;

function add(type, text = "") {
    const m = document.createElement("div");
    m.className = "msg " + type;
    const b = document.createElement("div");
    b.className = "bubble";
    b.textContent = text;
    m.appendChild(b);
    messages.appendChild(m);
    messages.scrollTop = messages.scrollHeight;
    return b;
}

function type(el, text) {
    el.textContent = "";
    let i = 0;
    const t = setInterval(() => {
        el.textContent += text[i++] || "";
        messages.scrollTop = messages.scrollHeight;
        if (i >= text.length) clearInterval(t);
    }, 15);
}

async function send() {
    if (locked || !input.value.trim()) return;

    locked = true;
    input.disabled = true;
    sendBtn.disabled = true;

    const text = input.value;
    input.value = "";

    add("user", text);
    const aiBubble = add("ai");

    try {
        const r = await fetch("/api/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ message: text })
        });

        const d = await r.json();
        type(aiBubble, d.reply || "Réponse vide.");

    } catch (e) {
        type(aiBubble, "Erreur JS : " + e.message);
    }

    setTimeout(() => {
        locked = false;
        input.disabled = false;
        sendBtn.disabled = false;
        input.focus();
    }, 300);
}

sendBtn.onclick = send;
input.addEventListener("keydown", e => {
    if (e.key === "Enter") send();
});
