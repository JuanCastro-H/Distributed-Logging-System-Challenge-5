# =======================================
# SERVICIO SIMULADO DE PAGO
# =======================================

# ---------------------------------------
# LIBRERISA E IMPORTACIONES
# ---------------------------------------

import requests
import random
import time
from datetime import datetime
from server.token_generator import get_or_create_token


# ---------------------------------------
# CONFIGURACION DEL SERVICIO
# ---------------------------------------

# --- Configuracion Base Del Servicio ---
SERVER_URL = "http://127.0.0.1:5000/logs"     # Endpoint del servidor.
SERVICE    = "payment-service"                # Nombre del servicio.
SERVICE_TOKEN  = None                         # Token de autenticacion.

# --- Severidad ---
SEVERITY_LEVELS = ["INFO", "DEBUG", "ERROR", "WARNING"]

# --- Mensajes simulados ---
MESSAGES = [
    "Payment processed sucessfully", # Pago procesado con éxito.
    "Card declined",                 # Tarjeta rechazada.
    "Insufficient funds",            # Fondos insuficientes.
    "Transaction timeout",           # Tiempo de espera de transacción.
    "You have an outstanding debt"   # Tienes una deuda pendiente.
]


# -----------------------------------------------
# FUNCION PARA GESTIONAR LOS TOKENS DEL SERVICIO
# -----------------------------------------------

def init_token(service_name):
    
    # --- Modificar Variable Global Del Token ---
    global SERVICE_TOKEN

    # --- Generar u Obtener El Token Del servicio ---
    SERVICE_TOKEN = get_or_create_token(service_name)


# -------------------------------------------
# FUNCION PARA GENERAR UN LOG ALEATORIO
# -------------------------------------------

def generate_log():

    # --- Contruir Log Con Datos Simulados ---
    return {
        "timestamp" : datetime.now().isoformat(),
        "service"   : SERVICE,
        "severity"  : random.choice(SEVERITY_LEVELS),
        "message"    : random.choice(MESSAGES)
    }


# ---------------------------------------
# FUNCION PARA ENVIAR LOG AL SERVIDOR
# ---------------------------------------

def send_log(log, service_name):

    # --- Construir El Headers ---
    headers = {
        "Authorization": f"Token {SERVICE_TOKEN}",
        "Content-type": "application/json"
    }

    # --- Enviar Request Al Servidor ---
    try:
        response = requests.post(
            SERVER_URL, 
            json=log, 
            headers=headers, 
            timeout=5 # Evita Bloqueos si el servidor no responde.
        )

    # --- Notificar Error Critico De Conexion ---
    except requests.exceptions.RequestException as e:
        print(f"[CRITICAL] No se pudo conectar al servidor: {e}")
        return

    # --- Procesar Respuesta Del Servidor ---
    try:
        response_data = response.json()
    except:
        response_data = response.text

    # --- Manejar Respuesta Del Servidor ---

    if response.status_code == 201:
        print(f"[OK] Log enviado ({service_name})")
    elif response.status_code == 400:
        print(f"[BAD REQUEST] {response_data}")
    elif response.status_code == 401:
        print(f"[UNAUTHORIZED] Token inválido")
    elif response.status_code == 500:
        print(f"[SERVER ERROR] {response_data}")
    else:
        print(f"[ERROR {response.status_code}] {response_data}")


# ---------------------------------------
# BLOQUE EJECUTOR
# ---------------------------------------

if __name__ == "__main__":

    # --- Inicializar Token ---
    init_token(SERVICE)

    # --- Bucle Para Enviar Logs ---
    while True:
        log = generate_log()          # Crea un log.
        send_log(log, SERVICE)        # Envia el log al servidor.
        time.sleep(7)                 # Tiempo de espera para repetir el bucle.