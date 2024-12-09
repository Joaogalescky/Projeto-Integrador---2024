const registerForm = document.getElementById('register-form');

registerForm.addEventListener('submit', async (event) => {
    event.preventDefault();

// document.addEventListener('DOMContentLoaded', function() {
//     document.getElementById('register-form').addEventListener('submit', function(event) {
//         event.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm-password').value;
        
        console.log(email, password, confirmPassword)
    
        try {
            const response = await fetch('/register/', {  // Substitua pela URL correta
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email,
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
// });