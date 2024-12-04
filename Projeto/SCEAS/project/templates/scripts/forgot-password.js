document.getElementById('forgot-password-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const errorDiv = document.getElementById('forgot-password-error');
    const successDiv = document.getElementById('forgot-password-success');

    // Dados para a API
    const data = {
        email: email
    };

    fetch('/api/password-reset/', { // Substitua pela rota real no Django
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
                throw new Error('Erro ao enviar email.');
            }
        })
        .then(data => {
            // Exibir mensagem de sucesso
            successDiv.style.display = 'block';
            successDiv.textContent = 'Instruções foram enviadas para seu email.';
            errorDiv.style.display = 'none';
        })
        .catch(error => {
            // Exibir mensagem de erro
            console.error('Erro:', error);
            errorDiv.style.display = 'block';
            errorDiv.textContent = error.message || 'Erro ao tentar enviar email.';
            successDiv.style.display = 'none';
        });
});
// Configurar o link de cadastro dinamicamente
document.getElementById('login-link').addEventListener('click', function () {
    window.location.href = './Login.html'; // Ajuste o caminho conforme necessário
});