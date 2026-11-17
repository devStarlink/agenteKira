import sqlite3 

from pathlib import Path

DB_PATH = Path("data/kira_memory.db")

def database_creation():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS configuracion (clave TEXT PRIMARY KEY, valor TEXT NOT NULL)""")

        conn.execute("""CREATE TABLE IF NOT EXISTS Hechos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        categoria TEXT NOT NULL,
                        contenido TEXT NOT NULL UNIQUE  
        )""")

def save_config(clave: str, valor: str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT OR REPLACE INTO configuracion (clave, valor) VALUES (?, ?)", (clave, valor))

def get_config(clave: str) -> str | None:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT valor FROM configuracion WHERE clave = ?", (clave,))
        row = cursor.fetchone()

        return row[0] if row else None

def save_fact(categoria: str, contenido: str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT OR IGNORE INTO hechos (categoria, contenido) VALUES (?, ?)",
            (categoria.strip(), contenido.strip()),
        )

def get_all_facts() -> list[str]:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            
            """
            SELECT contenido FROM hechos 
            WHERE categoria IN ('usuario', 'proposito', 'capacidades')
            UNION ALL
            SELECT contenido FROM (
                SELECT contenido FROM hechos 
                WHERE categoria NOT IN ('usuario', 'proposito', 'capacidades')
                ORDER BY id DESC LIMIT 10
            )
            """
        )

        return [row[0] for row in cursor.fetchall()]