let chats = JSON.parse(localStorage.getItem("phantom_chats")) || {};
let currentChatId = null;

const chatDiv = document.getElementById("chat");
const chatList = document.getElementById("chatList");

function save() {
  localStorage.setItem("phantom_chats", JSON.stringify(chats));
}

function newChat() {
  currentChatId = Date.now().toString();
  chats[currentChatId] = [];
  save();
  renderChatList();
  renderChat();
}

function renderChatList() {
  chatList.innerHTML = "";
  Object.keys(chats).forEach(id => {
    const div = document.createElement("div");
    div.className = "chat-item";
    div.textContent = "Chat " + id.slice(-4);
    div.onclick = () => {
      currentChatId = id;
      renderChat();
    };
    chatList.appendChild(div);
  });
}

function renderChat() {
  chatDiv.innerHTML = "";
  if (!currentChatId) return;

  chats[currentChatId].forEach(m => {
    chatDiv.innerHTML += `<div class="message ${m.role}">${m.text}</div>`;
  });
  chatDiv.scrollTop = chatDiv.scrollHeight;
}

async function sendMessage() {
  const input = document.getElementById("question");
  const text = input.value.trim();
  if (!text || !currentChatId) return;

  chats[currentChatId].push({ role: "user", text: "🧑 " + text });
  input.value = "";
  renderChat();
  save();

  const aiMsg = { role: "ai", text: "🤖 " };
  chats[currentChatId].push(aiMsg);
  renderChat();

  const res = await fetch("/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: text })
  });

  const reader = res.body.getReader();
  const decoder = new TextDecoder("utf-8");

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    aiMsg.text += decoder.decode(value);
    renderChat();
    save();
  }
}

document.getElementById("send").onclick = sendMessage;
document.getElementById("newChat").onclick = newChat;

document.getElementById("question").addEventListener("keydown", e => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

if (Object.keys(chats).length === 0) newChat();
else {
  currentChatId = Object.keys(chats)[0];
  renderChatList();
  renderChat();
}
