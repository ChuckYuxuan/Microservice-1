function askQuestion() {
    var question = document.getElementById('question').value;
    fetch('http://127.0.0.1:5000/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('answer').innerText = data.answer;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
