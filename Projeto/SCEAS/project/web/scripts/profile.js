document.getElementById('search-user-btn').addEventListener('click', function () {
    const userId = document.getElementById('user-id-input').value;
    const errorMessage = document.getElementById('error-message');
    const userInfo = document.getElementById('user-info');
    const userIdSpan = document.getElementById('user-id');
    const userNameSpan = document.getElementById('user-name');
    const userPhoneSpan = document.getElementById('user-phone');
    const userEmailSpan = document.getElementById('user-email');
    const vehicleList = document.getElementById('vehicle-list');

    errorMessage.style.display = 'none';
    userInfo.style.display = 'none';

    if (!userId) {
        errorMessage.textContent = 'Por favor, insira um ID de usuário.';
        errorMessage.style.display = 'block';
        return;
    }

    fetch(`/api/usuarios/${userId}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}` // Autorização com Token
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Usuário não encontrado.');
            }
            return response.json();
        })
        .then(data => {
            userIdSpan.textContent = data.id;
            userNameSpan.textContent = data.nome;
            userPhoneSpan.textContent = data.telefone;
            userEmailSpan.textContent = data.email;

            // Limpar lista de veículos
            vehicleList.innerHTML = '';
            if (data.veiculos && data.veiculos.length > 0) {
                data.veiculos.forEach(veiculo => {
                    const listItem = document.createElement('li');
                    listItem.className = 'list-group-item';
                    listItem.textContent = `Placa: ${veiculo.placa}, Modelo: ${veiculo.modelo}, Marca: ${veiculo.marca}, Cor: ${veiculo.cor}`;
                    vehicleList.appendChild(listItem);
                });
            } else {
                const noVehiclesItem = document.createElement('li');
                noVehiclesItem.className = 'list-group-item';
                noVehiclesItem.textContent = 'Nenhum veículo cadastrado.';
                vehicleList.appendChild(noVehiclesItem);
            }

            userInfo.style.display = 'block';
        })
        .catch(error => {
            errorMessage.textContent = error.message || 'Erro ao buscar usuário.';
            errorMessage.style.display = 'block';
        });
});
