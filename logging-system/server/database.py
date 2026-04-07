# =======================================
# BASE DE DATOS 
# =======================================

# --- Libreria De La BD ---
import sqlite3
from pathlib import Path

# --- Nombre De La Base De Datos ---
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "logs.db"

""# --- Nombre De La Base De Datos ---
#B_NAME = "logging-system/data/logs.db"""

# --- Crear Conexion Con La BD ---
def create_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn

# --- Crear Tabla --- 
def create_table():
    # --- Conectar Y Crear Cursor ---
    conn   = create_connection()
    cursor = conn.cursor()

    # --- Tabla ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        timestamp TEXT,
        service TEXT,
        severity TEXT,
        message TEXT,
        received_at TEXT
    )
    """)

    # --- Guardar los cambios y cerrar conexion ---
    conn.commit()
    conn.close()


if __name__ == "__main__":

    create_table()
    print("Base de datos y tabla creadas correctamente")