import os
import requests
import polars as pl
import time
from dotenv import load_dotenv
from pathlib import Path

# 🔹 Carregar variáveis de ambiente
load_dotenv()
PUBMED_API_KEY = os.getenv("PUBMED_API_KEY")
MAX_RESULTS = int(os.getenv("PUBMED_MAX_RESULTS", 50))  # Padrão: 50 artigos
RETRIES = 3  # Tentativas de requisição em caso de falha
DELAY = 5  # Tempo de espera entre tentativas
DETAILS_DELAY = 2  # Tempo de espera entre requisições de detalhes dos artigos

# 🔹 Estratégia de busca (ajustada para precisão e replicabilidade)
QUERY = (
    '("mobile applications"[Title/Abstract] OR "health apps"[Title/Abstract]) '
    'AND ("data analysis"[Title/Abstract])'
)

# 🔹 Definir caminho de saída para os arquivos
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

CSV_FILE = RAW_DATA_DIR / "pubmed_articles.csv"
PARQUET_FILE = RAW_DATA_DIR / "pubmed_articles.parquet"

def fetch_pubmed_articles(query, max_results=MAX_RESULTS, retries=RETRIES, delay=DELAY):
    """Extrai IDs dos artigos da API PubMed"""
    
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "api_key": PUBMED_API_KEY,
    }

    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if "esearchresult" not in data:
                print(f"⚠️ Tentativa {attempt+1}: Resposta inesperada da API PubMed:", data)
                time.sleep(delay)
                continue
            
            return data["esearchresult"]["idlist"]

        except requests.RequestException as e:
            print(f"⚠️ Erro na tentativa {attempt+1}: {e}")
            time.sleep(delay)

    print("❌ Todas as tentativas falharam. Verifique a API.")
    return []


def fetch_article_details(article_ids):
    """Coleta detalhes dos artigos da PubMed"""
    articles = []

    for idx, article_id in enumerate(article_ids):
        time.sleep(DETAILS_DELAY)  # Espera para evitar bloqueios
        article_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        article_params = {"db": "pubmed", "id": article_id, "retmode": "json"}
        
        try:
            article_response = requests.get(article_url, params=article_params, timeout=10)
            article_response.raise_for_status()
            article_data = article_response.json()

            if article_id in article_data.get("result", {}):
                article_info = article_data["result"][article_id]
                articles.append({
                    "id": article_id,
                    "title": article_info.get("title", "N/A"),
                    "journal": article_info.get("source", "N/A"),
                    "authors": ", ".join([a["name"] for a in article_info.get("authors", [])]) if "authors" in article_info else "N/A",
                    "pub_date": article_info.get("pubdate", "N/A"),
                    "source": "PubMed",
                })
        
        except requests.RequestException as e:
            print(f"⚠️ Erro ao buscar artigo {article_id}: {e}")
            continue

    return pl.DataFrame(articles)


if __name__ == "__main__":
    print("🔍 Iniciando extração de artigos da PubMed...")
    
    article_ids = fetch_pubmed_articles(QUERY)
    
    if not article_ids:
        print("❌ Nenhum artigo encontrado na PubMed.")
    else:
        print(f"✅ {len(article_ids)} IDs de artigos encontrados. Buscando detalhes...")
        pubmed_data = fetch_article_details(article_ids)

        if pubmed_data.is_empty():
            print("❌ Nenhum detalhe de artigo extraído.")
        else:
            # 📌 Salvar dados nos formatos CSV e Parquet
            pubmed_data.write_csv(CSV_FILE)
            pubmed_data.write_parquet(PARQUET_FILE)

            print(f"✅ {len(pubmed_data)} artigos salvos em:")
            print(f"   - {CSV_FILE}")
            print(f"   - {PARQUET_FILE}")
