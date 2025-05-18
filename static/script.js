document.addEventListener('DOMContentLoaded', function() {
    const messageHistory = document.getElementById('messageHistory');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');

    // Auto-resize textarea
    userInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });

    // Send message on Enter (but allow Shift+Enter for new lines)
    userInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    sendButton.addEventListener('click', sendMessage);

    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // Add user message to chat
        addMessage('user', message);
        userInput.value = '';
        userInput.style.height = 'auto';

        // Show typing indicator
        const typingIndicator = document.createElement('div');
        typingIndicator.className = 'message message-bot';
        typingIndicator.innerHTML = `
            <div class="message-avatar bot-avatar">♫</div>
            <div class="message-content bot-content typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;
        messageHistory.appendChild(typingIndicator);
        messageHistory.scrollTop = messageHistory.scrollHeight;

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });
            
            const data = await response.json();
            
            // Remove typing indicator
            messageHistory.removeChild(typingIndicator);
            
            // Add bot response
            addMessage('bot', data.response);
        } catch (error) {
            messageHistory.removeChild(typingIndicator);
            addMessage('bot', "Sorry, I encountered an error. Please try again.");
            console.error('Error:', error);
        }
    }

    function addMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message message-${sender}`;
        
        const avatar = sender === 'user' 
            ? '<div class="message-avatar user-avatar">You</div>'
            : '<div class="message-avatar bot-avatar">♫</div>';
        
        // Format links in responses
        const formattedText = text.replace(
            /(https?:\/\/[^\s]+)/g, 
            '<a href="$1" target="_blank" rel="noopener">$1</a>'
        );
        
        messageDiv.innerHTML = `
            ${avatar}
            <div class="message-content ${sender}-content">${formattedText}</div>
        `;
        
        messageHistory.appendChild(messageDiv);
        messageHistory.scrollTop = messageHistory.scrollHeight;
    }
});