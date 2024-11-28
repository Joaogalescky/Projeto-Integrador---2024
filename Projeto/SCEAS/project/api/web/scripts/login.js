document.getElementById('login-form').addEventListener('submit', function (event) {
    event.preventDefault();  // Impede o envio do formulário tradicional

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorDiv = document.getElementById('login-error');

    const data = {
        username: email,
        password: password
    };

    fetch('/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.token) {
            localStorage.setItem('token', data.token);   // Armazena o token no localStorage
            window.location.href = '/home/';  // Redireciona para a página home
        } else {
            errorDiv.style.display = 'block';
            errorDiv.textContent = 'Credenciais inválidas.';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        errorDiv.style.display = 'block';
        errorDiv.textContent = 'Erro ao tentar fazer login.';
    });
});