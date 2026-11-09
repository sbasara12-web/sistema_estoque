from repositories import produto_repository


def validar(nome, valor, quantidade, minimo, maximo):
    nome = str(nome or "").strip()

    if not nome:
        raise ValueError(
            "A denominação do produto não pode ficar vazia."
        )

    try:
        valor = float(str(valor).replace(",", "."))
        quantidade = int(quantidade)
        minimo = int(minimo)
        maximo = int(maximo)

    except (TypeError, ValueError):
        raise ValueError("Informe valores numéricos válidos.")

    if valor < 0:
        raise ValueError("O valor não pode ser negativo.")

    if quantidade < 0 or minimo < 0 or maximo < 0:
        raise ValueError("As quantidades não podem ser negativas.")

    if maximo < minimo:
        raise ValueError(
            "O estoque máximo deve ser maior ou igual ao mínimo."
        )

    return nome, valor, quantidade, minimo, maximo


def cadastrar(nome, valor, quantidade, minimo, maximo):
    dados = validar(nome, valor, quantidade, minimo, maximo)

    nome, valor, quantidade, minimo, maximo = dados

    if produto_repository.buscar_por_nome(nome):
        raise ValueError(
            "Já existe um produto com essa denominação."
        )

    return produto_repository.criar(
        nome, valor, quantidade, minimo, maximo
    )


def editar(id, nome, valor, minimo, maximo):
    nome, valor, _, minimo, maximo = validar(
        nome, valor, 0, minimo, maximo
    )

    existente = produto_repository.buscar_por_nome(nome)

    if existente and existente["id"] != int(id):
        raise ValueError(
            "Já existe outro produto com essa denominação."
        )

    if not produto_repository.buscar(id):
        raise ValueError("Produto não encontrado.")

    produto_repository.atualizar(
        id, nome, valor, minimo, maximo
    )