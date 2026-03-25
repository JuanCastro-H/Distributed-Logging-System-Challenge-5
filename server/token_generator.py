
# =======================================
# GENERADOR DE TOKENS
# =======================================

# ---------------------------------------
# LIBRERIAS
# ---------------------------------------

import json
from pathlib import Path

#
TOKENS_FILE = "tokens.json"


# ---------------------------------------
# CREAR TOKEN UNICO
# ---------------------------------------

def generate_token(service_name, index):
    
    token = f"{service_name}-{str(index).zfill(4)}" 

    return token


# ---------------------------------------
# CONVERTIR TOKEN A JSON
# ---------------------------------------

def save_token(token, service_name):
    
    tokens = {}

    if Path(TOKENS_FILE).exists():
        with open(TOKENS_FILE, "r") as f:
            tokens = json.load(f)

    tokens[token] = service_name

    with open(TOKENS_FILE, "w") as f:
        json.dump(tokens, f, indent=2)


# ---------------------------------------
# GENERAR UN TOKEN PARA UN SERVICIO
# ---------------------------------------

def create_tokens_for_service(service_name, n):

    for i in range(1, n + 1):
        token = generate_token(service_name, i)
        save_token(token, service_name)
        print(f"Token generado: {token} para {service_name}")




