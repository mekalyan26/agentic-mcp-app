/**
 * Agentic MCP Demo Frontend Script
 */

// Configuration
const API_BASE_URL = 'http://localhost:5000';

// DOM Elements
const chatMessages = document.getElementById('chat-messages');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const toolsList = document.getElementById('tools-list');
const refreshToolsBtn = document.getElementById('refresh-tools');

/**
 * Add a message to the chat display
 * @param {string} content - Message content
 * @param {string} type - Message type ('user', 'assistant', 'system', 'tool')
 */
function addMessage(content, type = 'assistant') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    const paragraph = document.createElement('p');
    paragraph.textContent = content;
    messageDiv.appendChild(paragraph);
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Add a tool result to the chat display
 * @param {Object} toolResult - Tool execution result
 */
function addToolResult(toolResult) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message tool';
    
    const header = document.createElement('strong');
    header.textContent = `Tool: ${toolResult.tool}`;
    messageDiv.appendChild(header);
    
    const resultPre = document.createElement('pre');
    resultPre.textContent = JSON.stringify(toolResult.result, null, 2);
    messageDiv.appendChild(resultPre);
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Send a chat message to the backend
 * @param {string} message - User message
 */
async function sendMessage(message) {
    try {
        addMessage(message, 'user');
        
        const response = await fetch(`${API_BASE_URL}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message }),
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Display the assistant's message
        addMessage(data.message, 'assistant');
        
        // If a tool was called, display the result
        if (data.requires_tool && data.tool_result) {
            addToolResult(data.tool_result);
        }
    } catch (error) {
        console.error('Error sending message:', error);
        addMessage('Sorry, there was an error processing your request. Please make sure the backend server is running.', 'system');
    }
}

/**
 * Load available tools from the backend
 */
async function loadTools() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/tools`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        displayTools(data.tools);
    } catch (error) {
        console.error('Error loading tools:', error);
        toolsList.innerHTML = '<p class="error">Failed to load tools. Is the backend running?</p>';
    }
}

/**
 * Display tools in the sidebar
 * @param {Array} tools - List of tool definitions
 */
function displayTools(tools) {
    toolsList.innerHTML = '';
    
    if (!tools || tools.length === 0) {
        toolsList.innerHTML = '<p>No tools available</p>';
        return;
    }
    
    tools.forEach(tool => {
        const toolCard = document.createElement('div');
        toolCard.className = 'tool-card';
        
        const toolName = document.createElement('h3');
        toolName.textContent = tool.name;
        toolCard.appendChild(toolName);
        
        const toolDesc = document.createElement('p');
        toolDesc.textContent = tool.description;
        toolCard.appendChild(toolDesc);
        
        toolsList.appendChild(toolCard);
    });
}

// Event Listeners
chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    if (message) {
        sendMessage(message);
        userInput.value = '';
    }
});

refreshToolsBtn.addEventListener('click', loadTools);

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadTools();
});
