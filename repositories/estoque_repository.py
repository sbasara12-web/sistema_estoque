from banco import conectar


def registrar(tipo, produto_id, usuario_id, quantidade, data_hora):
    conn = conectar()

    produto = conn.execute(
        "SELECT * FROM produtos WHERE id = ?",
        (produto_id,)
    ).fetchone()

    if not produto:
        conn.close()
        raise ValueError("Produto não encontrado.")

    atual = produto["quantidade"]

    if tipo == "saida" and quantidade > atual:
        conn.close()
        raise ValueError(
            f"Saída não permitida: estoque insuficiente. "
            f"Disponível: {atual}. Solicitado: {quantidade}."
        )

    if tipo == "entrada":
        novo = atual + quantidade
    else:
        novo = atual - quantidade

    conn.execute(
        "UPDATE produtos SET quantidade = ? WHERE id = ?",
        (novo, produto_id)
    )

    conn.execute("""
        INSERT INTO movimentacoes
        (produto_id, usuario_id, tipo, quantidade, data_hora)
        VALUES (?, ?, ?, ?, ?)
    """, (produto_id, usuario_id, tipo, quantidade, data_hora))

    conn.commit()
    conn.close()

    return novo


def listar_movimentacoes():
    conn = conectar()

    movimentacoes = conn.execute("""
        SELECT
            m.*,
            strftime('%d-%m-%Y %H:%M', m.data_hora) AS data_hora,
            p.nome AS produto_nome,
            u.usuario
        FROM movimentacoes m
        JOIN produtos p ON p.id = m.produto_id
        JOIN usuarios u ON u.id = m.usuario_id
        ORDER BY m.data_hora DESC, m.id DESC
    """).fetchall()

    conn.close()
    return movimentacoes


def relatorio(inicio, fim):
    conn = conectar()

    resultado = conn.execute("""
        SELECT
            p.id,
            p.nome,

            COALESCE(SUM(
                CASE WHEN m.tipo = 'entrada'
                THEN m.quantidade ELSE 0 END
            ), 0) AS entradas,

            COALESCE(SUM(
                CASE WHEN m.tipo = 'saida'
                THEN m.quantidade ELSE 0 END
            ), 0) AS saidas,

            COALESCE(SUM(
                CASE WHEN m.tipo = 'entrada'
                THEN m.quantidade ELSE -m.quantidade END
            ), 0) AS saldo,

            COALESCE(SUM(
                CASE WHEN m.tipo = 'entrada'
                THEN m.quantidade * p.valor ELSE 0 END
            ), 0) AS valor_entradas,

            COALESCE(SUM(
                CASE WHEN m.tipo = 'saida'
                THEN m.quantidade * p.valor ELSE 0 END
            ), 0) AS valor_saidas

        FROM produtos p

        LEFT JOIN movimentacoes m
        ON m.produto_id = p.id
        AND date(m.data_hora) BETWEEN ? AND ?

        GROUP BY p.id, p.nome
        ORDER BY p.nome
    """, (inicio, fim)).fetchall()

    conn.close()
    return resultado


def alertas():
    conn = conectar()

    resultado = conn.execute("""
        SELECT * FROM produtos
        WHERE quantidade <= estoque_minimo
        OR quantidade >= estoque_maximo
        ORDER BY nome
    """).fetchall()

    conn.close()
    return resultado