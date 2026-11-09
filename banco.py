import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("estoque.db")


def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def inicializar_banco():
    conn = conectar()

    conn.executescript("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            usuario TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL,
            perfil TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL COLLATE NOCASE UNIQUE,
            valor REAL NOT NULL CHECK(valor >= 0),
            quantidade INTEGER NOT NULL CHECK(quantidade >= 0),
            estoque_minimo INTEGER NOT NULL,
            estoque_maximo INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            usuario_id INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            data_hora TEXT NOT NULL,

            FOREIGN KEY(produto_id) REFERENCES produtos(id),
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        );
    """)

    from werkzeug.security import generate_password_hash

    admin = conn.execute(
        "SELECT id FROM usuarios WHERE usuario = ?",
        ("admin",)
    ).fetchone()

    if not admin:
        conn.execute("""
            INSERT INTO usuarios (nome, usuario, senha_hash, perfil)
            VALUES (?, ?, ?, ?)
        """, (
            "Administrador",
            "admin",
            generate_password_hash("admin123"),
            "administrador"
        ))

    conn.commit()
    conn.close()