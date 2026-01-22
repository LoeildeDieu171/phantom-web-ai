* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: "Segoe UI", sans-serif;
}

body {
    height: 100vh;
    background: #0f0f0f;
    color: #e5e5e5;
}

.app {
    display: flex;
    height: 100vh;
}

/* SIDEBAR */
.sidebar {
    width: 260px;
    background: #111;
    border-right: 1px solid #222;
    padding: 20px;
    display: flex;
    flex-direction: column;
}

.sidebar h2 {
    margin-bottom: 20px;
}

.new-chat {
    background: #1f1f1f;
    border: 1px solid #333;
    color: white;
    padding: 10px;
    border-radius: 8px;
    cursor: pointer;
    margin-bottom: 20px;
}

.new-chat:hover {
    background: #2a2a2a;
}

.history {
    flex: 1;
}

.chat-item {
    padding: 10px;
    border-radius: 6px;
    cursor: pointer;
    margin-bottom: 5px;
}

.chat-item:hover {
    background: #1a1a1a;
}

.chat-item.active {
    background: #2a2a2a;
}

/* MAIN */
.main {
    flex: 1;
    display: flex;
    flex-direction: column;
}

/* MESSAGES */
.messages {
    flex: 1;
    padding: 30px;
    overflow-y: auto;
}

.message {
    margin-bottom: 20px;
    display: flex;
}

.message.ai {
    justify-content: flex-start;
}

.message.user {
    justify-content: flex-end;
}

.bubble {
    max-width: 70%;
    padding: 15px;
    border-radius: 12px;
    line-height: 1.5;
}

.message.ai .bubble {
    background: #1e1e1e;
}

.message.user .bubble {
    background: #007aff;
    color: white;
}

/* INPUT */
.input-bar {
    border-top: 1px solid #222;
    padding: 15px;
    display: flex;
    gap: 10px;
}

.input-bar input {
    flex: 1;
    background: #1e1e1e;
    border: none;
    padding: 12px;
    border-radius: 10px;
    color: white;
    outline: none;
}

.input-bar button {
    background: #007aff;
    border: none;
    color: white;
    padding: 0 18px;
    border-radius: 10px;
    font-size: 18px;
    cursor: pointer;
}

.input-bar button:hover {
    background: #005fd1;
}
