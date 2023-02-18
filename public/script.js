const chat = document.querySelector('.chat');

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
