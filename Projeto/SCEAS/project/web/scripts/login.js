document.getElementById('login-form').addEventListener('submit', function (event) {
    event.preventDefault(); // Impede o envio padrão do formulário

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorDiv = document.getElementById('login-error');

    const data = {
        username: email, // Assumindo que o backend usa "username" para email
        password: password
    };

    fetch('/api-token-auth/', { // Rota padrão do Django Rest Framework Auth Token
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Credenciais inválidas');
            }
        })
        .then(data => {
            // Armazena o token no localStorage
            localStorage.setItem('token', data.token);

            // Redireciona para a página inicial
            window.location.href = './home.html';
        })
        .catch(error => {
            console.error('Erro:', error);
            errorDiv.style.display = 'block';
            errorDiv.textContent = error.message || 'Erro ao tentar fazer login.';
        });
});
// Configurar o link de cadastro dinamicamente
document.getElementById('register-link').addEventListener('click', function () {
    window.location.href = './Register.html'; // Ajuste o caminho conforme necessário
});