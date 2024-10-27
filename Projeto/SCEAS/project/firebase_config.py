import os
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app

# Caminho relativo ao diretório do projeto
cred_path = os.path.join(os.path.dirname(__file__), 'credentials', 'serviceAccountKey.json')

if not os.path.exists(cred_path):
    raise ValueError("Arquivo de credenciais do Firebase não foi encontrado.")

cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

db = firestore.client()
