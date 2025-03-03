import os
import requests
import polars as pl
import time
from pathlib import Path
from dotenv import load_dotenv

# 🔹 Carregar credenciais do .env (se necessário)
load_dotenv()

# 🔹 Diretórios de saída
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# 🔹 Caminhos dos arquivos de saída
CSV_FILE = RAW_DATA_DIR / "scielo_articles.csv"
PARQUET_FILE = RAW_DATA_DIR / "scielo_articles.parquet"

# 🔹 Configuração da busca
QUERY = "mobile applications OR health apps AND data analysis"
MAX_RESULTS = int(os.getenv("SCIELO_MAX_RESULTS", 50))  # Número máximo de artigos

# 🔹 URL da API SciELO
SCIELO_API_URL = "https://search.scielo.org/api/v1/search"

def fetch_scielo_articles(query, max_results=MAX_RESULTS, retries=3, delay=5):
    """ Extrai artigos da API SciELO e retorna um DataFrame """
    params = {
        "q": query,
        "lang": "en",
        "count": max_results,
        "format": "json"
    }

    for attempt in range(retries):
        try:
            response = requests.get(SCIELO_API_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if "articles" not in data:
                print(f"⚠️ Tentativa {attempt+1}: Resposta inesperada da API SciELO:", data)
                time.sleep(delay)
                continue
            break  # Se sucesso, sai do loop
        except requests.RequestException as e:
            print(f"⚠️ Erro na tentativa {attempt+1}: {e}")
            time.sleep(delay)
    else:
        print("❌ Todas as tentativas falharam. Verifique a API.")
        return pl.DataFrame()

    articles = []
    for item in data.get("articles", []):
        articles.append({
            "id": item.get("id", "N/A"),
            "title": item.get("title", {}).get("en", "N/A"),
            "journal": item.get("journal", {}).get("title", "N/A"),
            "authors": ", ".join(item.get("authors", [])) if "authors" in item else "N/A",
            "pub_date": item.get("date", "N/A"),
            "source": "SciELO",
        })

    return pl.DataFrame(articles)

if __name__ == "__main__":
    print("🔍 Iniciando extração de artigos do SciELO...")
    scielo_data = fetch_scielo_articles(QUERY)

    if scielo_data.is_empty():
        print("❌ Nenhum artigo retornado.")
    else:
        # 📌 Salvar os dados extraídos
        scielo_data.write_csv(CSV_FILE)
        scielo_data.write_parquet(PARQUET_FILE)

        print(f"✅ {len(scielo_data)} artigos salvos em:")
        print(f"   - {CSV_FILE}")
        print(f"   - {PARQUET_FILE}")
