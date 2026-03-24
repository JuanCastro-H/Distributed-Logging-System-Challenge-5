from flask import Flask, request, jsonify
from database import create_connection
from datetime import datetime

app = Flask(__name__)

# --- Tokens validos ---
VALID_TOKENS = ["aabc123", "xyz789"]


# =========================
# POST /logs
# =========================
@app.route("/logs", methods=["POST"])

def receive_logs():

    # --- Validar Header ---
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Token "):
        return jsonify({"error": "No se ha reconocido"}), 401
    
    token = auth_header.split(" ")[1]

    if token not in VALID_TOKENS:
        return jsonify({"error": "Token invalido"}), 403
    
    # --- Obtener JSON ---
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON invalido"}), 400
    
    required_fields = ["timestamp", "service", "severity", "message"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Flta el campo {field}"}), 400
    
    # --- Guardar en BD ---
    conn = create_connection()
    cursor = conn.cursor()

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

    conn.commit()
    conn.close()

    return jsonify({"status": "log guardaado"}), 201

# =========================
# POST /logs
# =========================

@app.route("/logs", methods=["GET"])
def get_logs():

    timestamp_start = request.args.get("timestamp_start")
    timestamp_end   = request.args.get("timestamp_end")
    service         = request.args.get("service")
    severity        = request.args.get("severity")

    query  = "SELECT * FROM logs WHERE 1=1"
    params = []

    if timestamp_start:
        query += " AND timestamp >= ?"
        params.append(timestamp_start)

    if timestamp_end:
        query += " AND timestamp <= ?"
        params.append(timestamp_end)
    
    if service:
        query += " AND service = ?"
        params.append(service)

    if severity:
        query += " AND severity = ?"
        params.append(severity)
    
    query += " ORDER BY timestamp DESC"

    conn   = create_connection()
    cursor = conn.cursor()

    cursor.execute(query, params)
    rows = cursor.fetchall()

    conn.close()

    logs = []
    for row in rows:
        logs.append({
            "id"          : row[0],
            "timestamp"   : row[1],
            "service"     : row[2],
            "severity"    : row[3],
            "message"     : row[4],
            "received_at" : row[5]
        })
    
    return jsonify(logs), 200


# =========================
# GET /stats
# =========================

@app.route("/stats", methods=["GET"])

def get_stats():

    conn   = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT service, COUNT(*) FROM logs GROUP BY service
    """)
    logs_by_service = cursor.fetchall()

    cursor.execute("""
    SELECT severity, COUNT(*) FROM logs GROPU BY severity
    """)
    logs_by_severity = cursor.fetchall()

    cursor.execute("""
    SELECT service, MAX(timestamp) FROM logs GROUP BY service
    """)
    last_log_by_service = cursor.fetchall()

    conn.close()

    return jsonify({
        "logs_by_service"     : logs_by_service,
        "logs_by_severity"    : logs_by_severity,
        "last_log_by_service" : last_log_by_service
    })

# =========================
# BLOQUE EJECUTOR
# =========================
if __name__ == "__main__":
    app.run(debug=True)