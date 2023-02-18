/* script.js */

const chat = document.querySelector('.chat');
const input = document.querySelector('input[type="text"]');
const container = document.querySelector('.container');
const sendButton = document.querySelector('button');

function addMessage(text, sender) {
  const message = document.createElement('div');
  message.classList.add('message');
  message.classList.add(sender);

  const content = document.createElement('p');
  content.textContent = text;

  message.appendChild(content);
  chat.appendChild(message);
}

addMessage('Hello, how can I help you?', 'bot');

function toggleDarkMode() {
  container.classList.toggle('dark');
  input.classList.toggle('dark');
  sendButton.classList.toggle('dark');
}

function toggleAlternateBackground() {
  container.classList.toggle('alternate');
  input.classList.toggle('alternate');
  sendButton.classList.toggle('alternate');
}

document.querySelector('#darkMode').addEventListener('change', toggleDarkMode);
document.querySelector('#alternateBackground').addEventListener('change', toggleAlternateBackground);
