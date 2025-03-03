import os
import requests
import polars as pl
import time
from dotenv import load_dotenv
from pathlib import Path

# 🔹 Carregar credenciais do .env
load_dotenv()
WOS_API_KEY = os.getenv("WOS_API_KEY")

QUERY = 'TS=("mobile applications" OR "health apps") AND TS=("data analysis")'

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
CSV_FILE = RAW_DATA_DIR / "wos_articles.csv"
PARQUET_FILE = RAW_DATA_DIR / "wos_articles.parquet"

def fetch_wos_articles(query, max_results=50):
    """Extrai artigos da API Web of Science"""
    
    url = "https://wos-api.clarivate.com/api/wos/query"
    headers = {"X-APIKey": WOS_API_KEY}
    params = {
        "query": query,
        "count": max_results,
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        return data.get("Data", {}).get("Records", [])

    except requests.RequestException as e:
        print(f"❌ Erro na API Web of Science: {e}")
        return []

def process_wos_articles(records):
    """Processa os artigos retornados pela API Web of Science"""
    articles = [
        {
            "id": record.get("UID", "N/A"),
            "title": record.get("Title", "N/A"),
            "journal": record.get("Source", "N/A"),
            "authors": record.get("Authors", "N/A"),
            "pub_date": record.get("PublicationDate", "N/A"),
            "source": "Web of Science",
        }
        for record in records
    ]
    return pl.DataFrame(articles)

if __name__ == "__main__":
    print("🔍 Iniciando extração de artigos da Web of Science...")
    
    articles = fetch_wos_articles(QUERY)

    if not articles:
        print("❌ Nenhum artigo encontrado na Web of Science.")
    else:
        wos_data = process_wos_articles(articles)

        if wos_data.is_empty():
            print("❌ Nenhum detalhe de artigo extraído.")
        else:
            wos_data.write_csv(CSV_FILE)
            wos_data.write_parquet(PARQUET_FILE)

            print(f"✅ {len(wos_data)} artigos salvos em:")
            print(f"   - {CSV_FILE}")
            print(f"   - {PARQUET_FILE}")
