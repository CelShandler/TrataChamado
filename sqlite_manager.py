import sqlite3
import os
from config import DB_PATH

def inicializar_banco():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chamados_fechados (
            numero INTEGER PRIMARY KEY,
            data_processamento DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def chamado_existe(numero):
    if not os.path.exists(DB_PATH):
        return False
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT numero FROM chamados_fechados WHERE numero = ?", (numero,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

def registrar_chamado_fechado(numero):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO chamados_fechados (numero) VALUES (?)", (numero,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass # Já existe
    finally:
        conn.close()

def registrar_lote_fechados(numeros):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    numeros_tuplas = [(num,) for num in numeros]
    cursor.executemany("INSERT OR IGNORE INTO chamados_fechados (numero) VALUES (?)", numeros_tuplas)
    conn.commit()
    conn.close()
