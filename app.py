from flask import Flask, redirect
from routes import register_routes
from sheets import buscar_url_por_codigo
from datetime import datetime

app = Flask(__name__)
register_routes(app)

@app.route("/<codigo>")
def redirecionador_global(codigo):
    link = buscar_url_por_codigo(codigo)
    if not link:
        return "Link não encontrado", 404

    # Trata validade: permite "nunca" ou data ISO
    if link["expira_em"].lower() != "nunca":
        try:
            expira = datetime.fromisoformat(link["expira_em"])
            if expira < datetime.now():
                return "Link expirado", 410
        except Exception as e:
            print(f"[ERRO] Falha ao interpretar 'expira_em': {e}")
            return "Erro ao processar validade do link", 500

    return redirect(link["url"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
