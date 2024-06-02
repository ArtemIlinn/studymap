// static/script.js
document.addEventListener('DOMContentLoaded', function() {
    const messageIcon = document.getElementById('message-icon');
    const chatContainer = document.getElementById('chat-container');
    let chatOpen = false;

    messageIcon.addEventListener('click', function() {
        if (chatOpen) {
            chatContainer.style.display = 'none';
            chatOpen = false;
        } else {
            chatContainer.style.display = 'block';
            chatOpen = true;
        }
    });

    const chatForm = document.getElementById('chat-form');
    const chatWindow = document.getElementById('chat-window');

    chatForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const userInput = document.getElementById('user-input').value;
        appendMessage(userInput, 'user');
        sendUserInputToChatbot(userInput);
        document.getElementById('user-input').value = '';
    });

    function sendUserInputToChatbot(userInput) {
        fetch('/explore/chatbot', {
            method: 'POST',
            body: new URLSearchParams({ user_input: userInput }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        })
            .then(response => response.json())
            .then(data => {
                const chatbotResponse = data.response;
                appendMessage(chatbotResponse, 'chatbot');
            });
    }

    function appendMessage(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.textContent = message;
        messageElement.classList.add(sender);
        chatWindow.appendChild(messageElement);
    }
});
