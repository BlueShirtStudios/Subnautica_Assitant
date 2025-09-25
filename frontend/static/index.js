document.getElementById("chatForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const chatInput = document.getElementById('chat-input');
    const responseDiv = document.getElementById('response');
    const chatboxContainer = document.querySelector('.chatbox-container');
    const userMessage = chatInput.value.trim();

    if (userMessage === ''){
        return;
    }
    else{
        const res = await fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ userMessage })
        });
        const data = await res.json();
    }

    
    document.getElementById("response").innerText = data.response || `Error: ${data.error}`;
    responseDiv.style.display = 'block';
    chatInput.value = '';
});