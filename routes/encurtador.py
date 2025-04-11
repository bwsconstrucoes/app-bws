from flask import Blueprint, request, jsonify
from sheets import buscar_url_por_codigo, adicionar_link

encurtador_routes = Blueprint('encurtador', __name__, url_prefix='/encurtador')

@encurtador_routes.route("/<codigo>")
def obter_link(codigo):
    link = buscar_url_por_codigo(codigo)
    if not link:
        return jsonify({"erro": "Link não encontrado"}), 404
    return jsonify(link)

@encurtador_routes.route("/novo", methods=["POST"])
def novo_link():
    codigo = request.form.get("codigo", "").strip()
    url = request.form.get("url", "").strip()
    expira_em = request.form.get("expira_em", "").strip()

    if not codigo or not url or not expira_em:
        return jsonify({"erro": "Campos obrigatórios: codigo, url, expira_em"}), 400

    sucesso = adicionar_link(codigo, url, expira_em)
    if sucesso:
        return jsonify({
            "status": "ok",
            "short_url": f"https://link.bwsconstrucoes.com.br/{codigo}",
            "original_url": url,
            "expira_em": expira_em
        })
    else:
        return jsonify({"erro": "Falha ao gravar na planilha"}), 500
