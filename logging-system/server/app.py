# =======================================
# SERVIDOR DE LOGGINGS 
# =======================================

# ---------------------------------------
# LIBRERISA E IMPORTACIONES
# ---------------------------------------

from flask import Flask, request, jsonify # Framework para crear la API.
from database import create_connection    # Funcion para conectar la BD.
from datetime import datetime             # Manejar timestamps.
import json                               # Traer tokens dinamicos.
from pathlib import Path                  # Verificar archivos.
from queue import Queue                   # Estructura FIFO para guardar logs en BD.
import threading                          # Permite ejecutar funciones en segundo plano.


# ---------------------------------------
# VARIABLES GLOBALES
# ---------------------------------------

# --- Cola Global De Logs ---
log_queue = Queue()

# --- Crear instancia del servidor ---
app = Flask(__name__)

# --- Tokens archivados validos ---
TOKENS_FILE = "logging-system/data/tokens.json"


# -------------------------
# CARGAR TOKENS
# -------------------------

def load_tokens():

    # --- Verificar Si El Archivo Existe ---
    if Path(TOKENS_FILE).exists():

        # --- Leer y devolver tokens ---
        with open(TOKENS_FILE, "r") as f:
            return json.load(f)
        
    return {}


# ---------------------------------------
# FUNCION: PARA GUARDR LOG EN LA BD
# ---------------------------------------

def save_log_to_bd(data):

    # --- Guardar en BD ---
    conn = create_connection()
    cursor = conn.cursor()

    # --- Insertar Log ---
    cursor.execute("""
    INSERT INTO logs (timestamp, service, severity, message, received_at)
    VALUES (?, ?, ?, ?, ?)
    """, (
        data["timestamp"],
        data["service"],
        data["severity"],
        data["message"],
        datetime.now().isoformat()
    ))

    # --- Guardar Cambios ---
    conn.commit()
    conn.close()


# ----------------------------------------
# WORKER: PROCESAMIENTO ASINCRONO DE LOGS
# ----------------------------------------

def log_worker():

    print("[WORKER] Iniciado y esperando logs...")

    # --- Bucle Infinito Para Procesar Logs ---
    while True:

        log = log_queue.get()          # Obtiene un log de la cola.
        suceso = False                 # Verificador de fallas.

        for intentos in range(3):
            try:
                save_log_to_bd(log)    # Guardar log en BD.
                suceso = True
                break
            except Exception as excep: # Manejo de errores.
                print(f"[ERROR] Fallo guardado log intento {intentos + 1}: {excep}") 

        if not suceso: # Si fallan los 3 reintentos.
            print("[CRITICO] Log perdido despues de 3 intentos")

        log_queue.task_done()          # Marcar tarea como completada.


# =========================================
# ENDPOINT: POST /logs
# Recibe Logs Desde Servicios Simulado.
# =========================================

@app.route("/logs", methods=["POST"])
def receive_logs():

    # ---------------------------------------
    # VALIDACION DE AUTENTICACION
    # ---------------------------------------

    # --- Obtener Header Autorizado ---
    auth_header = request.headers.get("Authorization")

    # --- Validar Formato Del Header ---
    if not auth_header or not auth_header.startswith("Token "):
        return jsonify({"error": "No se ha reconocido quien sos?"}), 401
    
    # --- Extraer Token ---
    token = auth_header.split(" ")[1]

    # --- Validar El Token ---
    if token not in VALID_TOKENS.values():
        return jsonify({"error": "Token invalido. Quien sos bro?"}), 403


    # ---------------------------------------
    # VALIDACION DEL PYLOAD
    # ---------------------------------------

    # --- Obtener JSON Y Validar ---
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON invalido"}), 400
    
    # --- Campos Del JSON ---
    required_fields = ["timestamp", "service", "severity", "message"]

    # --- Verificar Cada Campo ---
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Flta el campo {field}"}), 400
    
    # --- Mandar log A La Cola De Guardado ---

    log_queue.put(data)

    return jsonify({"status": "log guardaado"}), 201 # Respuesta inmediata al cliente.


# =======================================
# ENDPOINT: GET/logs
# Permite Consultar Logs Con Filtros
# =======================================

@app.route("/logs", methods=["GET"])
def get_logs():

    # ---------------------------------------
    # PARAMETRO DE FILTRADO
    # ---------------------------------------

    timestamp_start   = request.args.get("timestamp_start") 
    timestamp_end     = request.args.get("timestamp_end")
    service           = request.args.get("service")
    severity          = request.args.get("severity")
    received_at_start = request.args.get("received_at_start")
    received_at_end   = request.args.get("received_at_end")

    # ---------------------------------------
    # CONSTRUCCION DINAMICA DE QUERY
    # ---------------------------------------

    query  = "SELECT * FROM logs WHERE 1=1"
    params = []

    # --- Filtro Por Rango De Tiempo ---
    if timestamp_start:
        query += " AND timestamp >= ?"
        params.append(timestamp_start)

    # --- Filtro Hasta Fecha Final ---
    if timestamp_end:
        query += " AND timestamp <= ?"
        params.append(timestamp_end)
    
    # --- Filtro Por Servicio ---
    if service:
        query += " AND service = ?"
        params.append(service)

    # --- Filtro Por Severidad ---
    if severity:
        query += " AND severity = ?"
        params.append(severity)

    if received_at_start:
        query += " AND received_at >= ?"
        params.append(received_at_start)

    if received_at_end:
        query += " AND received_at <= ?"
        params.append(received_at_end)
    
    # --- Ordenar resultados ---
    query += " ORDER BY timestamp DESC"

    
    # ---------------------------------------
    # EJECUCION DE QUERY
    # ---------------------------------------

    # --- Crear Conexion Con BD ---
    conn   = create_connection()
    cursor = conn.cursor()

    # --- Ejecutar Consulta ---
    cursor.execute(query, params)
    rows = cursor.fetchall()

    # --- Cerrar Conexion ---
    conn.close()


    # ---------------------------------------
    # FORMATEO DE RESPUESTA
    # ---------------------------------------

    
    logs = []

    # --- Convertir Filas De BD a Estructura JSON ---
    for row in rows:
        logs.append({
            "id"          : row[0],
            "timestamp"   : row[1],
            "service"     : row[2],
            "severity"    : row[3],
            "message"     : row[4],
            "received_at" : row[5]
        })
    
    # --- Devolver JSON y Estado De La Respuesta ---
    return jsonify(logs), 200


# ===================================
# ENPOINT: GET /stats
# Devuelve Estadisticas.
# ===================================

@app.route("/stats", methods=["GET"])

def get_stats():

    # --- Conectar A La BD ---
    conn   = create_connection()
    cursor = conn.cursor()

    # --- LOGS Por Servicio ---
    cursor.execute("""
    SELECT service, COUNT(*) FROM logs GROUP BY service
    """)
    logs_by_service = cursor.fetchall()

    # --- LOGS Por Severidad ---
    cursor.execute("""
    SELECT severity, COUNT(*) FROM logs GROUP BY severity
    """)
    logs_by_severity = cursor.fetchall()

    # --- Ultimo Log Registrado Por Servicio ---
    cursor.execute("""
    SELECT service, MAX(timestamp) FROM logs GROUP BY service
    """)
    last_log_by_service = cursor.fetchall()

    conn.close()


    # ---------------------------------------
    # RESPUESTA FINAL
    # ---------------------------------------

    return jsonify({
        "logs_by_service"     : logs_by_service,
        "logs_by_severity"    : logs_by_severity,
        "last_log_by_service" : last_log_by_service
    })


# =======================================
# ENDPOINT: DELETE /logs
# Elimina logs antiguos de la base de datos
# =======================================

@app.route("/logs", methods=["DELETE"])
def delete_logs():

    # --- Obtener El Corte De Tiempo ---
    before = request.args.get("before")
    mode = request.args.get("mode")
    confirm = request.args.get("confirm")

    # --- Crear Conexion ---
    conn = create_connection()
    cursor = conn.cursor()

    # ------------------------
    # MODO 1: BORRAR todo
    # ------------------------

    if mode == "all":
        # --- Proteccion Extra Contra Borrado ---
        if confirm != "true":
            return jsonify({
                "error": "Confirmación requerida para borrar todo (confirm=true)"
            }), 403
        cursor.execute("DELETE FROM logs")

    # ------------------------------
    # MODO 2: BORRAR POR FECHA
    # ------------------------------
    else:
        # --- Dar Error Si No Hay Fecha Limite ---
        if not before:
            return jsonify({"error": "Falta parámetro 'before'"}), 400

        cursor.execute("""
            DELETE FROM logs
            WHERE timestamp < ?
        """, (before,))

    # --- Contador Del Borrado ---
    deleted = cursor.rowcount # Cuenta de cuantos registros fueron eliminados.

    # --- Guardar Cambios ---
    conn.commit()
    conn.close()

    # --- Respuesta Al Cliente ---
    return jsonify({
        "status": "ok",
        "deleted_logs": deleted # Cantidad de logs borrados.
    }), 200
    

# =========================
# BLOQUE EJECUTOR
# =========================
if __name__ == "__main__":

    # --- Tokens validos ---
    VALID_TOKENS = load_tokens()
    
    # --- Iniciar Worker / ---
    worker_thread = threading.Thread(target=log_worker, daemon=True) # Empleado silencioso.
    worker_thread.start()

    print("[SERVER] Worker iniciado correctamente")

    # --- Actualizar Cambios ---
    app.run(debug=False)