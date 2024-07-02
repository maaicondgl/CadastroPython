// login.js

document.getElementById('form-register').addEventListener('submit', function(event) {
    event.preventDefault();
    
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var rg = document.getElementById('rg').value;
    var cpf = document.getElementById('cpf').value;
    var name = document.getElementById('name').value;
    
    var formData = {
        userName: username,
        password: password,
        rg: rg,
        cpf: cpf,
        name: name
    };

    fetch('http:///localhost:3033/cadastros/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao criar cadastro');
        }
        return response.json();
    })
    .then(data => {
        window.location.href = '/index';
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('erro ao criar cadastro do cliente');
    });
});
