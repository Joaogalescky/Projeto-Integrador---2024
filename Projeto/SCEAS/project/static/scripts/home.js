// Referência para o corpo da tabela
const tableBody = document.getElementById("user-table-body");

// Fetch para obter dados do Firebase ou API
fetch('/usuarios/')
    .then(response => response.json())
    .then(data => {
        // Preenche a tabela com os dados
        data.forEach((usuario, index) => {
            usuario.veiculos.forEach(veiculo => {
                const row = `
                    <tr>
                        <td>${index + 1}</td>
                        <td>${usuario.nome}</td>
                        <td>${usuario.telefone}</td>
                        <td>${usuario.email}</td>
                        <td>${veiculo.placa}</td>
                        <td>${veiculo.modelo}</td>
                        <td>${veiculo.marca}</td>
                        <td>${veiculo.cor}</td>
                    </tr>
                `;
                tableBody.innerHTML += row;
            });
        });
    })
    .catch(error => console.error("Erro ao carregar dados:", error));

// Exportar para CSV
document.getElementById("download-csv").addEventListener("click", () => {
    let csvContent = "data:text/csv;charset=utf-8,";
    const rows = document.querySelectorAll("table tr");
    rows.forEach(row => {
        const cols = Array.from(row.querySelectorAll("td, th")).map(col => col.textContent);
        csvContent += cols.join(",") + "\n";
    });

    // Cria um link para download
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "planilha_entrada.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
});