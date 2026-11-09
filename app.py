from functools import wraps

from flask import (
    Flask,
    session,
    redirect,
    url_for,
    flash,
    request
)

from banco import inicializar_banco

from controllers.auth_controller import auth_bp
from controllers.produto_controller import produto_bp
from controllers.estoque_controller import estoque_bp


app = Flask(__name__)

app.config["SECRET_KEY"] = "chave_secreta_sistema_estoque_2026"


def login_obrigatorio(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if not session.get("usuario_id"):

            flash(
                "Faça login para acessar o sistema.",
                "erro"
            )

            return redirect(url_for("auth.login"))

        return func(*args, **kwargs)

    return wrapper


def administrador_obrigatorio(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if session.get("perfil") != "administrador":

            flash(
                "Você não tem permissão para realizar esta operação.",
                "erro"
            )

            return redirect(url_for("produtos.listar"))

        return func(*args, **kwargs)

    return wrapper


@app.before_request
def proteger_rotas():

    if request.endpoint in (
        "auth.login",
        "auth.logout",
        "static"
    ):
        return

    if request.endpoint is None:
        return

    if not session.get("usuario_id"):

        flash(
            "Faça login para continuar.",
            "erro"
        )

        return redirect(url_for("auth.login"))


@app.context_processor
def dados_usuario():

    return {
        "usuario_logado": session.get("usuario"),
        "perfil_logado": session.get("perfil")
    }


app.register_blueprint(auth_bp)
app.register_blueprint(produto_bp)
app.register_blueprint(estoque_bp)


@app.errorhandler(404)
def pagina_nao_encontrada(erro):

    return "Página não encontrada.", 404


@app.errorhandler(500)
def erro_servidor(erro):

    return "Ocorreu um erro interno. Tente novamente.", 500


if __name__ == "__main__":

    inicializar_banco()

    app.run(debug=True)