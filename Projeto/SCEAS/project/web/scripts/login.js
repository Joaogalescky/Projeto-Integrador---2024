document.getElementById('login-form').addEventListener('submit', function (event) {
    event.preventDefault(); // Impede o envio padrão do formulário

    const email = document.getElementById('email').value; // "email" no front, mapeado para "username" no backend
    const password = document.getElementById('password').value;
    const errorDiv = document.getElementById('login-error');

    const data = {
        username: email,
        password: password,
    };

    fetch('/auth/', { // Rota correta para o token (ajuste conforme o backend: `/auth/`)
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then((response) => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Credenciais inválidas');
            }
        })
        .then((data) => {
            // Salva o token no localStorage
            localStorage.setItem('token', data.token);

            // Redireciona para a página inicial
            window.location.href = './home.html';
        })
        .catch((error) => {
            console.error('Erro:', error);
            errorDiv.style.display = 'block';
            errorDiv.textContent = error.message || 'Erro ao tentar fazer login.';
        });
});

// Configurar o link de cadastro dinamicamente
document.getElementById('register-link').addEventListener('click', function () {
    window.location.href = './Register.html'; // Ajuste o caminho conforme necessário
});