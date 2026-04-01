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


# --- Crear instancia del servidor ---
app = Flask(__name__)

# --- Tokens archivados validos ---
TOKENS_FILE = "logging-system/data/tokens.json"

# --- Tokens validos ---
VALID_TOKENS = {}


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


# -------------------------
# GUARDAR TOKENS
# -------------------------

def save_token(token, service):

    # --- Cargar Tokens Existentes ---
    tokens = load_tokens()

    # --- Agregar Nuevo Token ---
    tokens[token] = service

    # --- Guardarlo En El Archivo JSON ---
    with open(TOKENS_FILE, "w") as f:
        json.dump(tokens, f, indent=2)


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


    # --- Registrar Token Si Es Nuevo ---
    if token not in VALID_TOKENS:

        # --- Obtener Nombre Del Servicio ---
        service_name = request.json.get("service", "unknown")

        # --- Guardar En Memoria  ---
        VALID_TOKENS[token] = service_name

        # --- Guardar En Archivo JSON ---
        save_token(token, service_name)

        # --- Log En Consola ---
        print(f"[INFO] Nuevo token registraado Rey: {token} para {service_name}")


    # --- Validar El Token ---
    if token not in VALID_TOKENS:
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
    

    # ---------------------------------------
    # INSERTAR LOG EN LA BD
    # ---------------------------------------

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

    return jsonify({"status": "log guardaado"}), 201


# =======================================
# ENDPOINT: GET/logs
# Permite Consultar Logs Con Filtros
# =======================================

@app.route("/logs", methods=["GET"])
def get_logs():

    # ---------------------------------------
    # PARAMETRO DE FILTRADO
    # ---------------------------------------

    timestamp_start = request.args.get("timestamp_start")
    timestamp_end   = request.args.get("timestamp_end")
    service         = request.args.get("service")
    severity        = request.args.get("severity")

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

# =========================
# BLOQUE EJECUTOR
# =========================
if __name__ == "__main__":

    # --- Actualizar Cambios ---
    app.run(debug=True)
