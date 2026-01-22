const chat = document.getElementById("chat");
const input = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const form = document.getElementById("chatForm");

let aiBusy = false;

/* CREATE MESSAGE */
function addMessage(text, type) {
  const div = document.createElement("div");
  div.className = `message ${type}`;
  div.textContent = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
  return div;
}

/* TYPE ANIMATION */
function typeText(el, text, speed = 20) {
  el.textContent = "";
  let i = 0;
  const timer = setInterval(() => {
    el.textContent += text[i];
    chat.scrollTop = chat.scrollHeight;
    i++;
    if (i >= text.length) clearInterval(timer);
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
    const reply =
      "Je réponds maintenant correctement. Le message s’affiche, l’écriture est animée et tu ne peux pas spam pendant que je parle.";

    typeText(aiBubble, reply);

    setTimeout(() => {
      aiBusy = false;
      input.disabled = false;
      sendBtn.disabled = false;
      input.focus();
    }, reply.length * 20 + 300);
  }, 500);
}

/* EVENTS */
form.addEventListener("submit", (e) => {
  e.preventDefault();
  sendMessage();
});

window.onload = () => {
  input.focus();
};
