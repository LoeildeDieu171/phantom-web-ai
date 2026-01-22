const chat = document.getElementById("chat");
const input = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");

let aiBusy = false;

function addMessage(text, type) {
  const div = document.createElement("div");
  div.className = `message ${type}`;
  div.textContent = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
  return div;
}

function typeText(element, text, speed = 22) {
  element.textContent = "";
  let i = 0;

  const interval = setInterval(() => {
    element.textContent += text[i];
    chat.scrollTop = chat.scrollHeight;
    i++;
    if (i >= text.length) clearInterval(interval);
  }, speed);
}

async function sendMessage() {
  const text = input.value.trim();
  if (!text || aiBusy) return;

  aiBusy = true;
  input.value = "";
  input.disabled = true;
  sendBtn.disabled = true;

  addMessage(text, "user");
  const aiBubble = addMessage("", "ai");

  try {
    const res = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });

    const data = await res.json();
    typeText(aiBubble, data.response);
  } catch (e) {
    aiBubble.textContent = "Erreur serveur.";
  }

  setTimeout(() => {
    aiBusy = false;
    input.disabled = false;
    sendBtn.disabled = false;
    input.focus();
  }, 500);
}

sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keydown", e => {
  if (e.key === "Enter") sendMessage();
});
