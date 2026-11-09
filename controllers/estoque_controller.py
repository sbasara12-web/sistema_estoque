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

from services import estoque_service


estoque_bp = Blueprint("estoque", __name__)


@estoque_bp.route("/movimentar", methods=["POST"])
def movimentar():

    try:

        estoque_service.movimentar(
            request.form.get("tipo"),
            request.form.get("produto_id"),
            session["usuario_id"],
            request.form.get("quantidade")
        )

        flash(
            "Movimentação registrada com sucesso.",
            "sucesso"
        )

    except Exception as e:

        flash(str(e), "erro")

    return redirect(url_for("produtos.listar"))


@estoque_bp.route("/movimentacoes")
def movimentacoes():

    return render_template(
        "produtos.html",
        produtos=produto_repository.listar(),
        alertas=estoque_repository.alertas(),
        movimentacoes=estoque_repository.listar_movimentacoes()
    )


@estoque_bp.route("/relatorio", methods=["GET", "POST"])
def relatorio():

    linhas = []

    inicio = request.values.get("inicio", "")
    fim = request.values.get("fim", "")

    if inicio and fim:

        if inicio > fim:

            flash(
                "A data inicial não pode ser posterior à data final.",
                "erro"
            )

        else:

            linhas = estoque_repository.relatorio(
                inicio, fim
            )

    return render_template(
        "produtos.html",
        produtos=produto_repository.listar(),
        alertas=estoque_repository.alertas(),
        relatorio=linhas,
        inicio=inicio,
        fim=fim
    )