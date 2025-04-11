import requests
import csv

# ID da planilha Google compartilhada publicamente
SHEET_ID = "1k-ydMq9JEhWGSt7P3D0ucYj2bWNMkhA9uk1kBJiOMb8"
SHEET_NAME = "Links"

def buscar_url_por_codigo(codigo):
    """
    Busca um link na planilha Google com base no código
    """
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.content.decode("utf-8").splitlines()
        reader = csv.DictReader(content)

        for row in reader:
            if row["código"].strip().lower() == codigo.lower():
                return {
                    "url": row["url"].strip(),
                    "expira_em": row["expira_em"].strip()
                }
    except Exception as e:
        print(f"[Erro] Falha ao buscar código na planilha: {e}")
    return None


def adicionar_link(codigo, url, expira_em):
    """
    (Simulado) Adiciona um novo link à planilha
    ⚠️ Para funcionar de verdade, é necessário configurar:
    - Google Apps Script
    - ou uma API como sheet.best
    """
    try:
        print(f"[Simulado] Adicionando link: {codigo} → {url} (expira em {expira_em})")
        return True  # Simula sucesso
    except Exception as e:
        print(f"[Erro] ao simular adição de link: {e}")
        return False
