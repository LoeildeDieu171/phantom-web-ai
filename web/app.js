const chat = document.getElementById("chat");
const input = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");

let aiBusy = false;

/* ADD MESSAGE */
function addMessage(text, type) {
  const div = document.createElement("div");
  div.className = `message ${type}`;
  div.textContent = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
  return div;
}

/* TYPE EFFECT */
function typeText(element, text, speed = 25) {
  element.textContent = "";
  let i = 0;

  const interval = setInterval(() => {
    element.textContent += text[i];
    chat.scrollTop = chat.scrollHeight;
    i++;
    if (i >= text.length) clearInterval(interval);
  }, speed);
}

/* SEND MESSAGE */
function sendMessage() {
  const text = input.value.trim();
  if (!text || aiBusy) return;

  aiBusy = true;
  input.value = "";
  input.disabled = true;
  sendBtn.disabled = true;

  addMessage(text, "user");

  const aiBubble = addMessage("", "ai");

  setTimeout(() => {
    const response =
      "Je suis Phantom AI. Ceci est une réponse générée avec un vrai effet d’écriture progressive, comme ChatGPT.";

    typeText(aiBubble, response);

    setTimeout(() => {
      aiBusy = false;
      input.disabled = false;
      sendBtn.disabled = false;
      input.focus();
    }, response.length * 25 + 300);
  }, 600);
}

/* EVENTS */
sendBtn.addEventListener("click", sendMessage);

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendMessage();
});
