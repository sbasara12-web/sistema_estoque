from banco import conectar


def listar():
    conn = conectar()

    produtos = conn.execute(
        "SELECT * FROM produtos ORDER BY nome"
    ).fetchall()

    conn.close()
    return produtos


def buscar(id):
    conn = conectar()

    produto = conn.execute(
        "SELECT * FROM produtos WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()
    return produto


def buscar_por_nome(nome):
    conn = conectar()

    produto = conn.execute(
        "SELECT * FROM produtos WHERE nome = ? COLLATE NOCASE",
        (nome,)
    ).fetchone()

    conn.close()
    return produto


def criar(nome, valor, quantidade, minimo, maximo):
    conn = conectar()

    cursor = conn.execute("""
        INSERT INTO produtos
        (nome, valor, quantidade, estoque_minimo, estoque_maximo)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, valor, quantidade, minimo, maximo))

    conn.commit()
    id_produto = cursor.lastrowid
    conn.close()

    return id_produto


def atualizar(id, nome, valor, minimo, maximo):
    conn = conectar()

    conn.execute("""
        UPDATE produtos
        SET nome = ?, valor = ?, estoque_minimo = ?,
        estoque_maximo = ?
        WHERE id = ?
    """, (nome, valor, minimo, maximo, id))

    conn.commit()
    conn.close()


def excluir(id):
    conn = conectar()

    conn.execute(
        "DELETE FROM produtos WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()