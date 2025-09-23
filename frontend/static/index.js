document.getElementById("chatForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const question = document.getElementById("user_question").value;

    const res = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ question })
    });

    const data = await res.json();

    document.getElementById("response").innerText =
        data.response || `Error: ${data.error}`;
});