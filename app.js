function addMessage(message) {
    const messagesDiv = document.getElementById('messages');
    const messageElement = document.createElement('div');
    messageElement.textContent = message;
    messagesDiv.appendChild(messageElement);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

async function sendMessage() {
    const userInput = document.getElementById('userInput').value;
    if (userInput) {
        addMessage(`You: ${userInput}`);
        document.getElementById('userInput').value = '';

        try {
            const response = await fetch('http://127.0.0.1:5000/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: userInput,
                    userInfo: {
                        age: document.getElementById('age').value,
                        height: document.getElementById('height').value,
                        weight: document.getElementById('weight').value,
                        date: document.getElementById('date').value,
                    }
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            addMessage(`MedBot: ${data.response}`);
        } catch (error) {
            console.error('Error:', error);
            addMessage(`MedBot: Sorry, there was an error: ${error.message}`);
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('userForm').addEventListener('submit', function(event) {
        event.preventDefault();
        document.getElementById('user-info').classList.add('hidden');
        document.getElementById('chat-window').classList.remove('hidden');
        addMessage(`MedBot: Thank you! Now, you can ask me health-related questions or tell me your symptoms.`);
    });

    document.getElementById('sendBtn').addEventListener('click', sendMessage);

    document.getElementById('userInput').addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            sendMessage();
        }
    });
});