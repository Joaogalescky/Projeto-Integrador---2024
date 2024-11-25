from flask import Flask, request, render_template
import json
from pyzbar.pyzbar import decode
from models.firebase_config import db  # Importa o Firestore já configurado

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # Recebe a imagem JPEG enviada pelo ESP32-CAM
        img_file = request.files['image']
        img_bytes = img_file.read()

        # Processa o QR Code
        img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
        qr_codes = decode(img)

        for qr in qr_codes:
            qr_data = qr.data.decode('utf-8')
            data = json.loads(qr_data)  # O JSON enviado pelo ESP32-CAM

            # Dados do usuário e veículo extraídos do JSON
            usuario_data = data.get("usuario", {})
            veiculo_data = data.get("veiculo", {})

            # Salva os dados do usuário no Firestore
            usuario_ref = db.collection('usuarios').document(usuario_data["email"])
            usuario_ref.set(usuario_data)

            # Salva os dados do veículo no Firestore
            veiculo_ref = db.collection('veiculos').document(veiculo_data["placa"])
            veiculo_ref.set(veiculo_data)

            return "Dados recebidos e registrados com sucesso!", 200
    except Exception as e:
        return f"Erro ao processar a imagem: {str(e)}", 400

@app.route('/')
def index():
    # Obtém os dados dos usuários e seus veículos do Firestore
    usuarios = db.collection('usuarios').stream()
    return render_template('index.html', usuarios=usuarios)

if __name__ == '__main__':
    app.run(debug=True)
