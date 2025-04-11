from flask import Blueprint, request, jsonify
from sheets import buscar_url_por_codigo

encurtador_routes = Blueprint('encurtador', __name__, url_prefix='/encurtador')

@encurtador_routes.route("/<codigo>")
def obter_link(codigo):
    link = buscar_url_por_codigo(codigo)
    if not link:
        return jsonify({"erro": "Link não encontrado"}), 404
    return jsonify(link)
