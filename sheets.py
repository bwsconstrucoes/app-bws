import requests
import csv

SHEET_ID = "1k-ydMq9JEhWGSt7P3D0ucYj2bWNMkhA9uk1kBJiOMb8"
SHEET_NAME = "Links"
WEBAPP_URL = "https://script.google.com/macros/s/AKfycby9h_L99DY8Dp0xW3N8ci6KZizyeRcmQB53f3phbh0XqcqkZkaHc7UDmfQpD3Amj5l5CQ/exec"

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
    Adiciona um novo link à planilha via Google Apps Script
    """
    try:
        payload = {
            "codigo": codigo,
            "url": url,
            "expira_em": expira_em
        }
        response = requests.post(WEBAPP_URL, data=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"[Erro] ao adicionar link via WebApp: {e}")
        return False
