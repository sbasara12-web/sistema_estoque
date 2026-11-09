from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from repositories import (
    produto_repository,
    estoque_repository
)

from services import produto_service


produto_bp = Blueprint("produtos", __name__)


@produto_bp.route("/produtos")
def listar():

    produtos = produto_repository.listar()

    alertas = estoque_repository.alertas()

    return render_template(
        "produtos.html",
        produtos=produtos,
        alertas=alertas
    )


@produto_bp.route("/produtos/cadastrar", methods=["POST"])
def cadastrar():

    try:

        produto_service.cadastrar(
            request.form.get("nome"),
            request.form.get("valor"),
            request.form.get("quantidade"),
            request.form.get("minimo"),
            request.form.get("maximo")
        )

        flash(
            "Produto cadastrado com sucesso.",
            "sucesso"
        )

    except Exception as e:

        flash(str(e), "erro")

    return redirect(url_for("produtos.listar"))


@produto_bp.route("/produtos/<int:id>/editar", methods=["POST"])
def editar(id):

    try:

        produto_service.editar(
            id,
            request.form.get("nome"),
            request.form.get("valor"),
            request.form.get("minimo"),
            request.form.get("maximo")
        )

        flash("Produto atualizado com sucesso.", "sucesso")

    except Exception as e:

        flash(str(e), "erro")

    return redirect(url_for("produtos.listar"))


@produto_bp.route("/produtos/<int:id>/excluir", methods=["POST"])
def excluir(id):

    if session.get("perfil") != "administrador":

        flash(
            "Somente administradores podem excluir produtos.",
            "erro"
        )

        return redirect(url_for("produtos.listar"))

    try:

        produto_repository.excluir(id)

        flash("Produto excluído com sucesso.", "sucesso")

    except Exception:

        flash(
            "Não é possível excluir: existem movimentações "
            "vinculadas a este produto.",
            "erro"
        )

    return redirect(url_for("produtos.listar"))