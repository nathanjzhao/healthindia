document.getElementById('userForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent the default form submission behavior

    // Collect user information from the form
    const age = document.getElementById('age').value;
    const height = document.getElementById('height').value;
    const weight = document.getElementById('weight').value;
    const date = document.getElementById('date').value;

    // Hide the user information form and show the chat window
    const userInfo = { age, height, weight, date };
    document.getElementById('user-info').classList.add('hidden');
    document.getElementById('chat-window').classList.remove('hidden');

    // Initialize chat with a welcome message
    addMessage(`MedBot: Thank you! Now, you can ask me health-related questions or tell me your symptoms.`);

    // Set up the event listener for the send button
    document.getElementById('sendBtn').addEventListener('click', sendMessage);
});

async function sendMessage() {
    // Get the user input from the chat input box
    const userInput = document.getElementById('userInput').value;
    if (userInput) {
        // Display the user's message in the chat window
        addMessage(`You: ${userInput}`);
        document.getElementById('userInput').value = ''; // Clear the input box

        try {
            // Send the message to the server
            const response = await fetch('/api/chat', {
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

            // Handle response from the server
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            // Display the response from MedBot in the chat window
            addMessage(`MedBot: ${data.response}`);
        } catch (error) {
            console.error('Error:', error);
            // Display an error message in the chat window
            addMessage('MedBot: Sorry, there was an error processing your request.');
        }
    }
}

// Function to add a message to the chat window
function addMessage(message) {
    const messagesDiv = document.getElementById('messages');
    const messageElement = document.createElement('div');
    messageElement.textContent = message;
    messagesDiv.appendChild(messageElement);
    messagesDiv.scrollTop = messagesDiv.scrollHeight; // Scroll to the latest message
}
