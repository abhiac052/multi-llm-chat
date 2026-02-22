let sessionId = Math.random().toString(36).substring(7);
let selectedModel = null;

// Toast notification function
function showToast(message, duration = 3000) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, duration);
}

// Modal functions
function showModal(title, message, onConfirm) {
    const overlay = document.getElementById('modal-overlay');
    const modalTitle = document.getElementById('modal-title');
    const modalMessage = document.getElementById('modal-message');
    const confirmBtn = document.getElementById('modal-confirm-btn');
    
    modalTitle.textContent = title;
    modalMessage.textContent = message;
    overlay.classList.add('show');
    
    // Remove old event listeners and add new one
    const newConfirmBtn = confirmBtn.cloneNode(true);
    confirmBtn.parentNode.replaceChild(newConfirmBtn, confirmBtn);
    
    newConfirmBtn.addEventListener('click', () => {
        onConfirm();
        closeModal();
    });
}

function closeModal() {
    document.getElementById('modal-overlay').classList.remove('show');
}

function addMessage(model, content, isUser) {
    const messagesDiv = document.getElementById(`${model}-messages`);
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'assistant-message'}`;
    messageDiv.textContent = content;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function showLoading(model) {
    const messagesDiv = document.getElementById(`${model}-messages`);
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message loading';
    loadingDiv.id = `${model}-loading`;
    loadingDiv.textContent = '💭 Thinking...';
    messagesDiv.appendChild(loadingDiv);
}

function removeLoading(model) {
    const loadingDiv = document.getElementById(`${model}-loading`);
    if (loadingDiv) loadingDiv.remove();
}

async function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    
    if (!message) {
        showToast('⚠️ Please enter a message');
        return;
    }
    
    const sendBtn = document.getElementById('send-btn');
    sendBtn.disabled = true;
    input.value = '';
    
    try {
        if (selectedModel) {
            // Continue with selected model
            addMessage(selectedModel, message, true);
            showLoading(selectedModel);
            
            const response = await fetch('/continue', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    message: message,
                    model: selectedModel,
                    session_id: sessionId
                })
            });
            
            const data = await response.json();
            removeLoading(selectedModel);
            addMessage(selectedModel, data.response, false);
        } else {
            // Compare all models
            ['openai', 'claude', 'gemini'].forEach(model => {
                addMessage(model, message, true);
                showLoading(model);
            });
            
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    message: message,
                    session_id: sessionId
                })
            });
            
            const data = await response.json();
            
            ['openai', 'claude', 'gemini'].forEach(model => {
                removeLoading(model);
                addMessage(model, data[model], false);
            });
        }
    } catch (error) {
        showToast('❌ Error: ' + error.message);
        ['openai', 'claude', 'gemini'].forEach(model => removeLoading(model));
    }
    
    sendBtn.disabled = false;
    input.focus();
}

function selectModel(model) {
    const modelNames = {
        'openai': 'OpenAI GPT-4o-mini',
        'claude': 'Claude 3.5 Haiku',
        'gemini': 'Google Gemini 2.5'
    };
    
    showModal(
        '🎯 Continue with Model',
        `Do you want to continue the conversation with ${modelNames[model]}?`,
        () => {
            selectedModel = model;
            
            // Hide other columns
            ['openai', 'claude', 'gemini'].forEach(m => {
                const column = document.getElementById(`${m}-column`);
                if (m !== model) {
                    column.classList.add('hidden');
                }
            });
            
            // Update mode indicator
            document.getElementById('mode-text').textContent = `Mode: Continuing with ${modelNames[model]}`;
            showToast(`✅ Now chatting with ${modelNames[model]}`);
        }
    );
}

function resetChat() {
    showModal(
        '🔄 Reset Chat',
        'Are you sure you want to reset the chat? All conversation history will be cleared.',
        () => {
            fetch('/reset', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({session_id: sessionId})
            });
            
            // Clear UI
            ['openai', 'claude', 'gemini'].forEach(model => {
                document.getElementById(`${model}-messages`).innerHTML = '';
                document.getElementById(`${model}-column`).classList.remove('hidden');
            });
            
            selectedModel = null;
            sessionId = Math.random().toString(36).substring(7);
            document.getElementById('mode-text').textContent = 'Mode: Compare All Models';
            showToast('✅ Chat reset successfully');
        }
    );
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}
