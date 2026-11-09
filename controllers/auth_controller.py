from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from services import auth_service


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        user = auth_service.autenticar(
            request.form.get("usuario", ""),
            request.form.get("senha", "")
        )

        if user:

            session.clear()

            session["usuario_id"] = user["id"]
            session["usuario"] = user["usuario"]
            session["perfil"] = user["perfil"]

            return redirect(url_for("produtos.listar"))

        flash("Usuário ou senha incorretos.", "erro")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():

    session.clear()

    flash("Você saiu do sistema.", "sucesso")

    return redirect(url_for("auth.login"))


@auth_bp.route("/usuarios/cadastrar", methods=["POST"])
def cadastrar_usuario():

    if session.get("perfil") != "administrador":

        flash(
            "Somente administradores podem cadastrar usuários.",
            "erro"
        )

        return redirect(url_for("produtos.listar"))

    try:

        auth_service.criar_usuario(
            request.form.get("nome"),
            request.form.get("novo_usuario"),
            request.form.get("nova_senha"),
            request.form.get("perfil")
        )

        flash("Usuário cadastrado com sucesso.", "sucesso")

    except Exception as e:

        flash(str(e), "erro")

    return redirect(url_for("produtos.listar"))