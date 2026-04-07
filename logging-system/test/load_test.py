# =======================================
# SIMULADOR DE CARGA (LOAD TEST)
# =======================================

# ---------------------------------------
# LIBRERIAS E IMPORTACIONES
# ---------------------------------------
import threading
import time
import sys
import os

# --- Asegurar Imports Del Proyecto ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# --- Importar funciones del servicio ---
from services.auth_service import generate_log, send_log, init_token, SERVICE


# ---------------------------------------
# CONFIGURACION DE LA PRUEBA
# ---------------------------------------

TOTAL_LOGS   = 300    # Cantidad total de logs a enviar
NUM_THREADS  = 5      # Numero de hilos
DELAY        = 0          # Delay entre envios (0 = max velocidad)

# --- Inicializar Token ---
init_token(SERVICE)

# ---------------------------------------
# FUNCION DE TRABAJO POR HILO
# ---------------------------------------

def worker(thread_id, logs_per_thread):

    # --- Log inicial del hilo ---
    print(f"[THREAD-{thread_id}] iniciado con {logs_per_thread} logs")

    for i in range(logs_per_thread):

        # --- Generar log ---
        log = generate_log()

        # --- Enviar log ---
        send_log(log, SERVICE)

        # --- Delay opcional ---
        if DELAY > 0:
            time.sleep(DELAY)

    print(f"[THREAD-{thread_id}] finalizado")


# ---------------------------------------
# FUNCION PRINCIPAL DE PRUEBA
# ---------------------------------------

def run_load_test():

    print("\n=======================================")
    print("INICIANDO PRUEBA DE CARGA")
    print("=======================================\n")

    start_time = time.time()

    threads = []
    logs_per_thread = TOTAL_LOGS // NUM_THREADS

    # --- Crear hilos ---
    for i in range(NUM_THREADS):

        t = threading.Thread(
            target=worker,
            args=(i, logs_per_thread)
        )

        threads.append(t)
        t.start()

    # --- Esperar a que todos terminen ---
    for t in threads:
        t.join()

    end_time = time.time()

    # ---------------------------------------
    # RESULTADOS
    # ---------------------------------------

    total_time = end_time - start_time

    print("\n=======================================")
    print("RESULTADOS DE LA PRUEBA")
    print("=======================================")
    print(f"Logs enviados: {TOTAL_LOGS}")
    print(f"Hilos usados : {NUM_THREADS}")
    print(f"Tiempo total : {total_time:.2f} segundos")
    print(f"Logs/segundo : {TOTAL_LOGS / total_time:.2f}")
    print("=======================================\n")


# ---------------------------------------
# BLOQUE EJECUTOR
# ---------------------------------------

if __name__ == "__main__":

    run_load_test()