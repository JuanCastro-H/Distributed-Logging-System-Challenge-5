
# =======================================
# GENERADOR DE TOKENS
# =======================================

# ---------------------------------------
# LIBRERIAS
# ---------------------------------------

import json
from pathlib import Path
import uuid


TOKENS_FILE = "tokens.json"        # Direccion De Los Tokens.
Path("data").mkdir(exist_ok=True)  # Crear Carpeta Para Data Si no Existe.


#
#
#

def get_or_create_token(service_name):
    
    path = Path(TOKENS_FILE)

    if path.exists():
        with open(path, "r") as f:
            tokens = json.load(f)
    
    else:
        tokens = {}

    # Si ya existe → lo reutiliza
    if service_name in tokens:
        return tokens[service_name]

    # Si no existe → lo crea
    token = f"{service_name}-{uuid.uuid4().hex[:16]}"
    tokens[service_name] = token

    with open(path, "w") as f:
        json.dump(tokens, f, indent=2)

    return token










