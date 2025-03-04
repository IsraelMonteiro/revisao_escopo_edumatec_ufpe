import os
import requests
import polars as pl
import time
from dotenv import load_dotenv
from pathlib import Path

# 🔹 Carregar variáveis de ambiente
load_dotenv()

# 🔹 Configuração da API SciELO
BASE_URL = "http://articlemeta.scielo.org/api/v1/article/"
COLLECTION = "scl"

# 🔹 Lista de códigos de artigos para extração
ARTICLE_CODES = [
    "S0103-40142005000200002",
    "S0103-40142005000200003",
    "S0103-40142005000200004"
]

# 🔹 Diretório de saída
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

CSV_FILE = RAW_DATA_DIR / "scielo_articles.csv"
PARQUET_FILE = RAW_DATA_DIR / "scielo_articles.parquet"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_scielo_article(article_code, retries=3, delay=5):
    """Busca metadados de um artigo específico pelo código PID."""
    url = f"{BASE_URL}?code={article_code}&collection={COLLECTION}"

    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            return response.json()  # Retorna JSON estruturado do artigo

        except requests.RequestException as e:
            print(f"⚠️ Erro na tentativa {attempt+1} para {article_code}: {e}")
            time.sleep(delay)

    print(f"❌ Falha ao buscar artigo {article_code} após {retries} tentativas.")
    return None

def extract_field(data, field_list, default="N/A"):
    """Extrai um campo do JSON tentando múltiplas chaves possíveis."""
    for field in field_list:
        if field in data:
            value = data[field]
            if isinstance(value, list) and len(value) > 0:
                return value[0].get("_", default)
            return value.get("_", default) if isinstance(value, dict) else value
    return default

def format_date(date_str):
    """Converte uma data no formato YYYYMMDD para YYYY-MM-DD."""
    if date_str and len(date_str) >= 6:
        return f"{date_str[:4]}-{date_str[4:6]}"
    return date_str

def process_article_data(article_data):
    """Extrai informações essenciais do artigo retornado pela API."""
    if not article_data:
        return None

    article_info = article_data.get("article", {})

    # 🔹 Extração dos metadados principais
    title = extract_field(article_info, ["v12", "v100", "v901"], "Título não encontrado")
    journal = extract_field(article_info, ["v30", "v150", "v151"], "Periódico não encontrado")

    # 🔹 Extração dos autores
    authors = "N/A"
    if "v10" in article_info:
        authors_list = [a.get("n", "N/A") for a in article_info["v10"] if a.get("n")]
        authors = ", ".join(authors_list) if authors_list else "N/A"

    # 🔹 Extração e formatação da data de publicação
    pub_date = format_date(extract_field(article_info, ["v65"], ""))
    if pub_date == "":
        pub_date = article_data.get("processing_date", "Data não encontrada")

    return {
        "title": title,
        "journal": journal,
        "authors": authors,
        "publication_date": pub_date
    }

def extract_scielo_articles():
    """Extrai artigos da SciELO e salva em CSV e Parquet."""
    print("\n🔍 **Iniciando extração de artigos do SciELO...**\n")

    articles = []
    for code in ARTICLE_CODES:
        article_data = fetch_scielo_article(code)
        processed_data = process_article_data(article_data)
        if processed_data:
            articles.append(processed_data)

    if not articles:
        print("❌ Nenhum artigo extraído.")
        return

    # 🔹 Criando DataFrame Polars
    df = pl.DataFrame(articles)

    # 🔹 Salvando os dados
    df.write_csv(CSV_FILE)
    df.write_parquet(PARQUET_FILE)

    print("\n✅ Extração concluída!")
    print(f"📁 {len(articles)} artigos salvos em:")
    print(f"   - CSV: {CSV_FILE}")
    print(f"   - Parquet: {PARQUET_FILE}")

if __name__ == "__main__":
    extract_scielo_articles()
