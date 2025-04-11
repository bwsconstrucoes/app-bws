from flask import Blueprint, request, jsonify, redirect
import json
from datetime import datetime, timedelta
import os

encurtador_routes = Blueprint('encurtador', __name__, url_prefix='/encurtador')
DATA_FILE = "data/links.json"

def carregar_links():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def salvar_links(links):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(links, f, indent=2)

def limpar_expirados(links):
    agora = datetime.now()
    expirados = []

    for codigo in list(links):
        expira_em = links[codigo].get("expira_em")
        if expira_em == "nunca":
            continue
        try:
            if datetime.fromisoformat(expira_em) < agora:
                expirados.append(codigo)
                del links[codigo]
        except:
            continue
    if expirados:
        salvar_links(links)
    return expirados

@encurtador_routes.route("/", methods=["GET"])
def home():
    return '''
        <h2>Encurtador de Links BWS</h2>
        <form action="/novo" method="post">
            Código: <input name="codigo"><br>
            URL longa: <input name="url"><br>
            Validade (número de dias ou 'nunca'): <input name="dias_validade"><br>
            <input type="submit" value="Criar">
        </form>
    '''

@encurtador_routes.route("/novo", methods=["POST"])
def novo():
    codigo = request.form["codigo"].strip()
    url = request.form["url"].strip()
    dias = request.form.get("dias_validade", "").strip().lower()

    if not codigo or not url:
        return "Código e URL são obrigatórios", 400

    links = carregar_links()

    if dias == "nunca":
        expira_em = "nunca"
    elif dias.isdigit() and int(dias) > 0:
        expira_em = (datetime.now() + timedelta(days=int(dias))).isoformat()
    else:
        return "Preencha o campo de validade com 'nunca' ou um número de dias.", 400

    links[codigo] = {
        "url": url,
        "expira_em": expira_em
    }
    salvar_links(links)
    short_url = f"https://link.bwsconstrucoes.com.br/{codigo}"

    return jsonify({
        "status": "ok",
        "short_url": short_url,
        "original_url": url,
        "expira_em": expira_em
    })

@encurtador_routes.route("/<codigo>")
def redirecionar(codigo):
    links = carregar_links()
    limpar_expirados(links)
    if codigo in links:
        return redirect(links[codigo]["url"])
    return "Link não encontrado ou expirado", 404
