import os
import polars as pl
import logging
from pathlib import Path
from dotenv import load_dotenv
from health_edu_apps_etl.extract_pubmed import fetch_pubmed_articles
from health_edu_apps_etl.extract_scopus import fetch_scopus_articles
from health_edu_apps_etl.extract_wos import fetch_wos_articles
from health_edu_apps_etl.extract_ieee import fetch_ieee_articles
from health_edu_apps_etl.extract_scholar import fetch_scholar_articles
from health_edu_apps_etl.extract_scielo import fetch_scielo_articles

# 📌 Configuração de logs
logging.basicConfig(
    filename="etl_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# 🔹 Carregar variáveis de ambiente
load_dotenv()

# 🔹 Diretórios de saída
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

# 🔹 Caminho dos arquivos combinados
CSV_FILE = PROCESSED_DATA_DIR / "all_articles.csv"
PARQUET_FILE = PROCESSED_DATA_DIR / "all_articles.parquet"

# 🔹 Configurações globais
MAX_RESULTS = int(os.getenv("MAX_RESULTS", 50))

def run_etl():
    """Executa o pipeline ETL para todas as bases de dados"""
    logging.info("🚀 Iniciando pipeline ETL...")

    # 🔍 Etapa 1: Extração dos artigos
    print("🔍 Extraindo artigos...")
    datasets = []

    # 📌 PubMed
    print("📡 Extraindo da PubMed...")
    pubmed_data = fetch_pubmed_articles(MAX_RESULTS)
    if not pubmed_data.is_empty():
        pubmed_data.write_csv(RAW_DATA_DIR / "pubmed_articles.csv")
        pubmed_data.write_parquet(RAW_DATA_DIR / "pubmed_articles.parquet")
        datasets.append(pubmed_data)
        logging.info(f"✅ {len(pubmed_data)} artigos extraídos da PubMed.")

    # 📌 Scopus
    print("📡 Extraindo da Scopus...")
    scopus_data = fetch_scopus_articles(MAX_RESULTS)
    if not scopus_data.is_empty():
        scopus_data.write_csv(RAW_DATA_DIR / "scopus_articles.csv")
        scopus_data.write_parquet(RAW_DATA_DIR / "scopus_articles.parquet")
        datasets.append(scopus_data)
        logging.info(f"✅ {len(scopus_data)} artigos extraídos da Scopus.")

    # 📌 Web of Science
    print("📡 Extraindo da Web of Science...")
    wos_data = fetch_wos_articles(MAX_RESULTS)
    if not wos_data.is_empty():
        wos_data.write_csv(RAW_DATA_DIR / "wos_articles.csv")
        wos_data.write_parquet(RAW_DATA_DIR / "wos_articles.parquet")
        datasets.append(wos_data)
        logging.info(f"✅ {len(wos_data)} artigos extraídos da Web of Science.")

    # 📌 IEEE Xplore
    print("📡 Extraindo do IEEE Xplore...")
    ieee_data = fetch_ieee_articles(MAX_RESULTS)
    if not ieee_data.is_empty():
        ieee_data.write_csv(RAW_DATA_DIR / "ieee_articles.csv")
        ieee_data.write_parquet(RAW_DATA_DIR / "ieee_articles.parquet")
        datasets.append(ieee_data)
        logging.info(f"✅ {len(ieee_data)} artigos extraídos do IEEE Xplore.")

    # 📌 Google Scholar
    print("📡 Extraindo do Google Scholar...")
    scholar_data = fetch_scholar_articles(MAX_RESULTS)
    if not scholar_data.is_empty():
        scholar_data.write_csv(RAW_DATA_DIR / "scholar_articles.csv")
        scholar_data.write_parquet(RAW_DATA_DIR / "scholar_articles.parquet")
        datasets.append(scholar_data)
        logging.info(f"✅ {len(scholar_data)} artigos extraídos do Google Scholar.")

    # 📌 SciELO
    print("📡 Extraindo do SciELO...")
    scielo_data = fetch_scielo_articles(MAX_RESULTS)
    if not scielo_data.is_empty():
        scielo_data.write_csv(RAW_DATA_DIR / "scielo_articles.csv")
        scielo_data.write_parquet(RAW_DATA_DIR / "scielo_articles.parquet")
        datasets.append(scielo_data)
        logging.info(f"✅ {len(scielo_data)} artigos extraídos do SciELO.")

    # 🔍 Etapa 2: Consolidação dos artigos
    print("📊 Consolidando dados...")
    if datasets:
        combined_data = pl.concat(datasets, how="vertical").unique(subset=["id"])
        combined_data.write_csv(CSV_FILE)
        combined_data.write_parquet(PARQUET_FILE)
        logging.info(f"📦 {len(combined_data)} artigos combinados salvos em `{CSV_FILE}` e `{PARQUET_FILE}`.")
        print(f"✅ {len(combined_data)} artigos salvos com sucesso!")
    else:
        print("❌ Nenhum dado extraído. Verifique as APIs.")
        logging.warning("⚠️ Nenhum dado foi extraído.")

if __name__ == "__main__":
    run_etl()
