import cv2 # Visão computacional
import numpy as np # Manipulação de arrays
import pyzbar.pyzbar as pyz # Decodificar códigos de barras
import urllib.request # Requisições HTTP

# Captura de vídeo
#cap = cv2.VideoCapture(0) 
font = cv2.FONT_HERSHEY_PLAIN # Fonte

prev = "" # Armazena o último QR Code lido
pres = "" # Armazena o QR Code atual