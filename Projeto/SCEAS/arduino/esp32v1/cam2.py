import cv2
import numpy as np
import pyzbar.pyzbar as pyz
from pyzbar.pyzbar import decode

# Configurações iniciais

# Inicializa a câmera
cap = cv2.VideoCapture(0)

while True:
    # Captura o frame da câmera
    ret, frame = cap.read()

    # Decodifica os códigos QR presentes no frame
    qr_codes = decode(frame)

    # Processa os resultados
    for qr in qr_codes:
        # Extrai o conteúdo do código QR
        data = qr.data.decode('utf-8')

        # Desenha um retângulo em torno do código QR
        cv2.rectangle(frame, tuple(qr.polygon[0]), tuple(qr.polygon[2]), (0, 255, 0), 2)

        # Escreve o conteúdo do código QR na tela
        cv2.putText(frame, data, (qr.polygon[0][0], qr.polygon[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, (0, 255, 0), 2)

    # Exibe o frame com os códigos QR
    cv2.imshow('QR Code Scanner', frame)

    # Verifica se a tecla 'q' foi pressionada para encerrar o programa
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera os recursos utilizados
cap.release()
cv2.destroyAllWindows()