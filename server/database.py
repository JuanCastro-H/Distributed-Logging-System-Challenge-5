import sqlite3

# --- Nombre De La Base De Datos ---
DB_NAME = "logs.db"

# --- Crear Conexion Con La BD ---
def create_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
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