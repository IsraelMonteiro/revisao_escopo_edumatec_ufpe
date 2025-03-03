import os
import requests
import polars as pl
import time
from dotenv import load_dotenv
from pathlib import Path

# 🔹 Carregar credenciais do .env
load_dotenv()
SCOPUS_API_KEY = os.getenv("SCOPUS_API_KEY")
MAX_RESULTS = int(os.getenv("SCOPUS_MAX_RESULTS", 50))

# 🔹 Estratégia de busca
QUERY = 'TITLE-ABS-KEY(("mobile applications" OR "health apps") AND ("data analysis"))'

# 🔹 Diretório de saída
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
CSV_FILE = RAW_DATA_DIR / "scopus_articles.csv"
PARQUET_FILE = RAW_DATA_DIR / "scopus_articles.parquet"

def fetch_scopus_articles(query, max_results=MAX_RESULTS, retries=3, delay=5):
    """Extrai artigos da API Scopus"""
    
    url = "https://api.elsevier.com/content/search/scopus"
    headers = {"X-ELS-APIKey": SCOPUS_API_KEY}
    params = {
        "query": query,
        "count": max_results,
        "start": 0,
        "httpAccept": "application/json",
    }

    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if "search-results" not in data:
                print(f"⚠️ Tentativa {attempt+1}: Resposta inesperada da API Scopus:", data)
                time.sleep(delay)
                continue
            
            return data["search-results"]["entry"]

        except requests.RequestException as e:
            print(f"⚠️ Erro na tentativa {attempt+1}: {e}")
            time.sleep(delay)

    print("❌ Todas as tentativas falharam. Verifique a API.")
    return []

def process_articles(entries):
    """Processa os artigos retornados pela API Scopus"""
    articles = [
        {
            "id": entry.get("dc:identifier", "N/A"),
            "title": entry.get("dc:title", "N/A"),
            "journal": entry.get("prism:publicationName", "N/A"),
            "authors": entry.get("dc:creator", "N/A"),
            "pub_date": entry.get("prism:coverDate", "N/A"),
            "source": "Scopus",
        }
        for entry in entries
    ]
    return pl.DataFrame(articles)

if __name__ == "__main__":
    print("🔍 Iniciando extração de artigos da Scopus...")
    
    articles = fetch_scopus_articles(QUERY)

    if not articles:
        print("❌ Nenhum artigo encontrado na Scopus.")
    else:
        scopus_data = process_articles(articles)

        if scopus_data.is_empty():
            print("❌ Nenhum detalhe de artigo extraído.")
        else:
            scopus_data.write_csv(CSV_FILE)
            scopus_data.write_parquet(PARQUET_FILE)

            print(f"✅ {len(scopus_data)} artigos salvos em:")
            print(f"   - {CSV_FILE}")
            print(f"   - {PARQUET_FILE}")
