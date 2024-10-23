import cv2 # Visão computacional
import numpy as np # Manipulação de arrays
import pyzbar.pyzbar as pyz # Decodificar códigos de barras
import urllib.request # Requisições HTTP

#cap = cv2.VideoCapture(0) # Captura de vídeo 
font = cv2.FONT_HERSHEY_PLAIN # Fonte

url = 'http://192.168.1.109/' # URL de acesso
cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE) # Criar janela

prev = "" # Armazena o último QR Code lido
pres = "" # Armazena o QR Code atual

while True:
    img_resp = urllib.request.urlopen(url + 'cam-hi.jpg') # Requisição para a URL
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8) # Converte os dados
    frame = cv2.imdecode(imgnp, -1) # Decodifica o array para o OpenCV usar
    decodedObjects = pyz.decode(frame) # Biblioteca para decodificar
    for obj in decodedObjects: # Iteração para QR Code
        pres=obj.data # Armazena o QR Code
        if prev == pres:
            pass
        else: # Imprima os dados
            print("Type:",obj.type)
            print("Data: ",obj.data)
            prev=pres # Armazene
        cv2.putText(frame, str(obj.data), (50, 50), font, 2, (255, 0, 0), 3) # Adicione o texto na posição (50, 50)
    cv2.imshow("live transmission", frame)