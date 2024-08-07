document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');
    const chatButton = document.getElementById('chat-button');
    const chatWindow = document.getElementById('chat-window');
    const chatBody = document.getElementById('chat-body');
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');

    console.log(chatButton, chatWindow, chatBody, chatInput, sendButton); // Check if elements are found

    chatButton.addEventListener('click', function() {
        chatWindow.classList.toggle('hidden');
    });

    sendButton.addEventListener('click', function() {
        const userInput = chatInput.value.trim();
        if (userInput) {
            appendMessage('You', userInput);
            chatInput.value = '';
            fetch('http://localhost:5005/webhooks/rest/webhook', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: userInput })
            })
            .then(response => response.json())
            .then(data => {
                data.forEach((msg) => {
                    appendMessage('Bot', msg.text);
                });
            })
            .catch(error => {
                console.error('Error:', error);
                appendMessage('Bot', 'Sorry, there was an error. Please try again.');
            });
        } else {
            appendMessage('Bot', 'Please enter a message.');
        }
    });
});
