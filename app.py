from flask import Flask, redirect
from routes import register_routes
import json
from datetime import datetime

app = Flask(__name__)
register_routes(app)

@app.route("/<codigo>")
def redirecionador_global(codigo):
    try:
        with open("data/links.json", "r") as f:
            links = json.load(f)
        link = links.get(codigo)
        if not link:
            return "Link não encontrado", 404

        if link["expira_em"] != "nunca":
            expira = datetime.fromisoformat(link["expira_em"])
            if expira < datetime.now():
                return "Link expirado", 410

        return redirect(link["url"])
    except:
        return "Erro ao acessar banco de links", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
