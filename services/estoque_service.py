from datetime import datetime

from repositories import estoque_repository


def movimentar(tipo, produto_id, usuario_id, quantidade):

    if tipo not in ("entrada", "saida"):
        raise ValueError("Tipo de movimentação inválido.")

    try:
        produto_id = int(produto_id)
        quantidade = int(quantidade)

    except (TypeError, ValueError):
        raise ValueError(
            "Produto e quantidade devem ser números válidos."
        )

    if quantidade <= 0:
        raise ValueError(
            "A quantidade deve ser maior que zero."
        )

    data_hora = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return estoque_repository.registrar(
        tipo,
        produto_id,
        usuario_id,
        quantidade,
        data_hora
    )