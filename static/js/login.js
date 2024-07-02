// login.js

document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    
    var formData = {
        userName: username,
        password: password
    };

    fetch('http://localhost:3033/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao fazer login');
        }
        return response.json();
    })
    .then(data => {
        window.location.href = '/profile/' + data.userId;
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Usuário ou senha incorretos');
    });
});
