from banco import conectar


def buscar_por_usuario(usuario):
    conn = conectar()

    resultado = conn.execute(
        "SELECT * FROM usuarios WHERE usuario = ?",
        (usuario,)
    ).fetchone()

    conn.close()
    return resultado


def listar():
    conn = conectar()

    resultado = conn.execute(
        "SELECT id, nome, usuario, perfil FROM usuarios"
    ).fetchall()

    conn.close()
    return resultado


def criar(nome, usuario, senha_hash, perfil):
    conn = conectar()

    cursor = conn.execute("""
        INSERT INTO usuarios (nome, usuario, senha_hash, perfil)
        VALUES (?, ?, ?, ?)
    """, (nome, usuario, senha_hash, perfil))

    conn.commit()
    id_usuario = cursor.lastrowid
    conn.close()

    return id_usuario