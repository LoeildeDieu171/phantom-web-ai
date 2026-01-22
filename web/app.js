/* ============================================================
   PHANTOM AI - FRONTEND LOGIC
   Author: ChatGPT (for Phantom Project)
   File: web/app.js
   Purpose:
   - Chat UI logic
   - Input lock while AI responds
   - Typing animation (realistic)
   - Error-proof frontend
   ============================================================ */

/* ============================================================
   GLOBAL STATE
   ============================================================ */

const PhantomApp = {
    apiUrl: "/api/chat",
    isBusy: false,
    typingSpeed: 18,
    messageQueue: [],
    currentAbort: null,
    elements: {}
};

/* ============================================================
   SAFE DOM ACCESS
   ============================================================ */

function $(id) {
    return document.getElementById(id);
}

function safe(el) {
    return el !== null && el !== undefined;
}

/* ============================================================
   INITIALIZATION
   ============================================================ */

document.addEventListener("DOMContentLoaded", () => {
    PhantomApp.elements = {
        input: $("userInput"),
        sendBtn: $("sendBtn"),
        chat: $("chat"),
        status: $("status")
    };

    if (!safe(PhantomApp.elements.input)) {
        console.error("Input not found");
        return;
    }

    bindEvents();
    setStatus("Phantom AI prêt.");
});

/* ============================================================
   EVENT BINDINGS
   ============================================================ */

function bindEvents() {
    PhantomApp.elements.sendBtn.addEventListener("click", sendMessage);

    PhantomApp.elements.input.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
}

/* ============================================================
   UI STATE CONTROL
   ============================================================ */

function lockUI() {
    PhantomApp.isBusy = true;
    PhantomApp.elements.input.disabled = true;
    PhantomApp.elements.sendBtn.disabled = true;
    setStatus("Phantom AI réfléchit…");
}

function unlockUI() {
    PhantomApp.isBusy = false;
    PhantomApp.elements.input.disabled = false;
    PhantomApp.elements.sendBtn.disabled = false;
    PhantomApp.elements.input.focus();
    setStatus("Phantom AI prêt.");
}

function setStatus(text) {
    if (safe(PhantomApp.elements.status)) {
        PhantomApp.elements.status.textContent = text;
    }
}

/* ============================================================
   MESSAGE HANDLING
   ============================================================ */

function sendMessage() {
    if (PhantomApp.isBusy) return;

    const text = PhantomApp.elements.input.value.trim();
    if (!text) return;

    PhantomApp.elements.input.value = "";

    appendMessage("user", text);
    lockUI();

    fetchAIResponse(text);
}

/* ============================================================
   FETCH AI RESPONSE
   ============================================================ */

async function fetchAIResponse(message) {
    try {
        const response = await fetch(PhantomApp.apiUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message })
        });

        if (!response.ok) {
            throw new Error("HTTP error " + response.status);
        }

        const data = await response.json();

        if (!data || typeof data.reply !== "string") {
            throw new Error("Invalid server response");
        }

        animateAIResponse(data.reply);

    } catch (err) {
        console.error(err);
        appendMessage("ai", "Erreur serveur contrôlée.\nRéessaie.");
        unlockUI();
    }
}

/* ============================================================
   CHAT UI RENDERING
   ============================================================ */

function appendMessage(role, text) {
    const msg = document.createElement("div");
    msg.className = `message ${role}`;

    const bubble = document.createElement("div");
    bubble.className = "bubble";

    bubble.textContent = text;
    msg.appendChild(bubble);

    PhantomApp.elements.chat.appendChild(msg);
    scrollToBottom();
}

/* ============================================================
   TYPING ANIMATION (FAKE STREAM)
   ============================================================ */

function animateAIResponse(fullText) {
    const msg = document.createElement("div");
    msg.className = "message ai";

    const bubble = document.createElement("div");
    bubble.className = "bubble";

    msg.appendChild(bubble);
    PhantomApp.elements.chat.appendChild(msg);
    scrollToBottom();

    let index = 0;

    function typeNext() {
        if (index < fullText.length) {
            bubble.textContent += fullText.charAt(index);
            index++;
            scrollToBottom();
            setTimeout(typeNext, PhantomApp.typingSpeed);
        } else {
            unlockUI();
        }
    }

    typeNext();
}

/* ============================================================
   SCROLL MANAGEMENT
   ============================================================ */

function scrollToBottom() {
    PhantomApp.elements.chat.scrollTop =
        PhantomApp.elements.chat.scrollHeight;
}

/* ============================================================
   SAFETY: GLOBAL ERROR HANDLER
   ============================================================ */

window.addEventListener("error", (event) => {
    console.error("Global error:", event.error);
    unlockUI();
});

/* ============================================================
   DEV TOOLS (OPTIONAL)
   ============================================================ */

window.PhantomDebug = {
    lock: lockUI,
    unlock: unlockUI,
    state: PhantomApp
};

/* ============================================================
   END OF FILE
   ============================================================ */
