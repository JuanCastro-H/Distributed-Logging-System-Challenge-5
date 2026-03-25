# =======================================
# SERVICIO SIMULADO DE AUTENTICACION
# =======================================

# ---------------------------------------
# LIBRERISA E IMPORTACIONES
# ---------------------------------------
import requests
import random
import time
from datetime import datetime
import json
import uuid

# ---------------------------------------
# CONFIGURACION DEL SERVICIO
# ---------------------------------------

SERVER_URL = "http://127.0.0.1:5000/logs" 
SERVICE    = "auth-service"               

"""# --- Cargar Tokens Dinamicos ---
with open("tokens.json") as f:
    tokens = json.load(f)"""

"""# --- Filtrar tokens correspondientes a este servicio ---
SERVICE_TOKENS = [t for t, s in tokens.items() if s == SERVICE]"""

# --- Severidad ---
SEVERITY_LEVELS = ["INFO", "DEBUG", "ERROR", "WARNING"]

# --- Mensajes ---
MESSAGES = [
    "User logged in successfully",
    "Invalid password attempt",
    "Token expired",
    "User logged out",
    "Database conection failed"
]


# -------------------------------------------
# FUNCION PARA GENERAR UN LOG ALEATORIO
# -------------------------------------------

def generate_log():

    #
    return {
        "timestamp": datetime.now().isoformat(),
        "service"  : SERVICE,
        "severity" : random.choice(SEVERITY_LEVELS),
        "message"  : random.choice(MESSAGES)
    }


# ---------------------------------------
# GENERAR UN TOKEN UNICO POR LOG
# ---------------------------------------
def generate_token(service_name):
    
    return f"{service_name}-{uuid.uuid4().hex[:8]}"

# ---------------------------------------
# FUNCION PARA ENVIAR LOG AL SERVIDOR
# ---------------------------------------

def send_log(log, service_name):

    # --- Elegir Un Token Del Servicio ---
    token = generate_token(service_name)

    #
    headers = {
        "Authorization" : f"Token {token}",
        "Content-type"  : "application/json"
    }

    #
    response = requests.post(SERVER_URL, json=log, headers=headers)

    #
    if response.status_code == 201:
        print(f"[OK] Log enviado con token {token}: {log}")
    else:
        print(f"[ERROR] {response.status_code}: {response.json()}")


# ---------------------------------------
# BLOQUE EJECUTOR
# ---------------------------------------

if __name__ == "__main__":

    # --- Bucle para enviar logs ---
    while True:
        log = generate_log()          # Genera el log.
        send_log(log, SERVICE)        #
        time.sleep(5)                 # Espera 5/s antes de repetir el bucle.