
# =======================================
# GENERADOR DE TOKENS
# =======================================

# ---------------------------------------
# LIBRERIAS
# ---------------------------------------

import json
from pathlib import Path
import uuid

# --- Direccion De Los Tokens ---
BASE_DIR = Path(__file__).resolve().parent.parent
TOKENS_FILE = BASE_DIR / "data" / "tokens.json"

Path("data").mkdir(exist_ok=True)                # Crear Carpeta Para Data Si no Existe.


# ---------------------------------------
# OBTENER O CREAR TOKEN
# ---------------------------------------

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










