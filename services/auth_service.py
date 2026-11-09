from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

from repositories import usuario_repository


def autenticar(usuario, senha):
    user = usuario_repository.buscar_por_usuario(usuario)

    if user and check_password_hash(user["senha_hash"], senha):
        return user

    return None


def criar_usuario(nome, usuario, senha, perfil):
    nome = nome.strip()
    usuario = usuario.strip()

    if not nome or not usuario or not senha:
        raise ValueError("Preencha todos os campos.")

    if len(senha) < 6:
        raise ValueError("A senha deve ter pelo menos 6 caracteres.")

    if perfil not in ("operador", "administrador"):
        raise ValueError("Perfil inválido.")

    if usuario_repository.buscar_por_usuario(usuario):
        raise ValueError("Este usuário já existe.")

    senha_hash = generate_password_hash(senha)

    return usuario_repository.criar(
        nome, usuario, senha_hash, perfil
    )