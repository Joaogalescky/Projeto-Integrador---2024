const registerForm = document.getElementById('registerForm');

registerForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    
    try {
        const response = await fetch('/api/register/', {  // Substitua pela URL correta
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email,
                first_name: firstName,
                password,
            }),
        });

        if (response.ok) {
            console.log('Cadastro bem-sucedido:', await response.json());
        } else {
            console.error('Erro no cadastro:', await response.json());
        }
        if (password !== confirmPassword) {
            alert('As senhas não coincidem.');
            return;
        }
    } catch (error) {
        console.error('Erro na requisição:', error);
    }
});

// Link de cadastro dinamicamente
// document.getElementById('login-link').addEventListener('click', function () {
//     const url = this.getAttribute('data-url');
//     window.location.href = url;
// });