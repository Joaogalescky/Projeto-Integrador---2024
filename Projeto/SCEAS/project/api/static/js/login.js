// Configuração do Firebase
const firebaseConfig = {
    apiKey: "AIzaSyAm4JouCBP2uqzbdgERpx_Jc8mSOEMooOU",
    authDomain: "sceas-49731.firebaseapp.com",
    projectId: "sceas-49731",
    storageBucket: "sceas-49731.appspot.com",
    messagingSenderId: "238120420766",
    appId: "1:238120420766:web:5e805821439670d613c28f"
};

firebase.initializeApp(firebaseConfig);

document.querySelector('#login-form').addEventListener('submit', function (e) {
    e.preventDefault(); // Impede o envio padrão do formulário

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Autenticar com Firebase
    firebase.auth().signInWithEmailAndPassword(email, password)
        .then((userCredential) => {
            loginWithDjangoBackend(email, password);
        })
        .catch((error) => {
            const errorMsg = document.getElementById('login-error');
            errorMsg.style.display = 'block';
            errorMsg.textContent = 'Erro: ' + error.message;
        });
});

// Enviar as credenciais ao backend Django
function loginWithDjangoBackend(email, password) {
    fetch('/api/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({ email: email, password: password })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = '/home/';
            } else {
                const errorMsg = document.getElementById('login-error');
                errorMsg.style.display = 'block';
                errorMsg.textContent = 'Erro: ' + data.message;
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            const errorMsg = document.getElementById('login-error');
            errorMsg.style.display = 'block';
            errorMsg.textContent = 'Erro ao se comunicar com o servidor';
        });
}