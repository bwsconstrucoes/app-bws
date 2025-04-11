import requests
import csv
from datetime import datetime

SHEET_ID = "1k-ydMq9JEhWGSt7P3D0ucYj2bWNMkhA9uk1kBJiOMb8"
SHEET_NAME = "Links"

def buscar_url_por_codigo(codigo):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.content.decode("utf-8").splitlines()
        reader = csv.DictReader(content)

        for row in reader:
            if row["código"].strip() == codigo:
                return {
                    "url": row["url"].strip(),
                    "expira_em": row["expira_em"].strip()
                }
    except Exception as e:
        print(f"Erro ao buscar código na planilha: {e}")
    return None
