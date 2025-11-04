const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

function addMessage(sender, text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = sender;
    msgDiv.textContent = text;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
    const msg = userInput.value.trim();
    if (!msg) return;
    addMessage('user', msg);
    userInput.value = '';

    fetch('http://localhost:5000/chat', {  // Replace with deployed backend URL after hosting
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg })
    })
    .then(res => res.json())
    .then(data => addMessage('bot', data.reply))
    .catch(err => addMessage('bot', 'Error connecting to server.'));
}
