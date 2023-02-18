const chat = document.querySelector('.chat');
const input = document.querySelector('input[type="text"]');
const sendButton = document.querySelector('button');
const darkModeToggle = document.getElementById('dark-mode-toggle');
const backgroundUpload = document.getElementById('background-upload');
const customizationPanel = document.querySelector('.customization-panel');

function addMessage(text, sender) {
	const message = document.createElement('div');
	message.classList.add('message');
	message.classList.add(sender);

	const content = document.createElement('p');
	content.textContent = text;

	message.appendChild(content);
	chat.appendChild(message);
}

sendButton.addEventListener('click', () => {
	if (input.value) {
		addMessage(input.value, 'me');
		input.value = '';
		setTimeout(() => addMessage('I am a chatbot', 'bot'), 1000);
	}
});

input.addEventListener('keydown', (event) => {
	if (event.key === 'Enter' && input.value) {
		addMessage(input.value, 'me');
		input.value = '';
		setTimeout(() => addMessage('I am a chatbot', 'bot'), 1000);
	}
});

darkModeToggle.addEventListener('change', () => {
	document.body.classList.toggle('dark-mode');
});

backgroundUpload.addEventListener('change', () => {
	const file = backgroundUpload.files[0];
	const reader = new FileReader();

	reader.addEventListener('load', () => {
		document.body.style.backgroundImage = `url(${reader.result})`;
	});

	if (file) {
		reader.readAsDataURL(file);
	}
});

customizationPanel.addEventListener('click', (event) => {
	event.stopPropagation();
});

document.addEventListener('click', () => {
	customizationPanel.classList.remove('open');
});

document.addEventListener('keydown', (event) => {
	if (event.key === 'Escape') {
		customizationPanel.classList.remove('open');
	}
});

document.querySelector('.container').addEventListener('click', (event) => {
	event.stopPropagation();
	customizationPanel.classList.toggle('open');
});
