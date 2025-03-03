import os
import polars as pl
from pathlib import Path

# 🔹 Diretórios
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

# 🔹 Arquivos de entrada e saída
RAW_FILES = [
    RAW_DATA_DIR / "pubmed_articles.parquet",
    RAW_DATA_DIR / "scielo_articles.parquet",
]
OUTPUT_FILE = PROCESSED_DATA_DIR / "articles.parquet"

def clean_text(text):
    """ Remove espaços extras e caracteres estranhos. """
    return text.strip().replace("\n", " ").replace("\r", " ") if isinstance(text, str) else text

def standardize_date(date_str):
    """ Converte datas para formato YYYY-MM-DD. """
    try:
        return pl.Series(date_str).str.to_date(format="%Y-%m-%d").to_list()[0]
    except Exception:
        return None

def load_and_clean_data():
    """ Carrega, transforma e salva os dados processados. """
    all_articles = []

    for file in RAW_FILES:
        if file.exists():
            print(f"📥 Carregando {file}...")
            df = pl.read_parquet(file)

            # 🛠️ Limpeza e normalização
            df = df.with_columns([
                pl.col("title").apply(clean_text).alias("title"),
                pl.col("journal").apply(clean_text).alias("journal"),
                pl.col("authors").apply(clean_text).alias("authors"),
                pl.col("pub_date").apply(standardize_date).alias("pub_date"),
            ]).drop_nulls()

            all_articles.append(df)

    if not all_articles:
        print("⚠️ Nenhum arquivo válido encontrado.")
        return

    # 🔹 Concatenar todos os artigos e remover duplicatas
    final_df = pl.concat(all_articles, how="vertical").unique(subset=["title"])

    # 🔹 Salvar dataset transformado
    final_df.write_parquet(OUTPUT_FILE)
    print(f"✅ Transformação concluída! {len(final_df)} artigos salvos em `{OUTPUT_FILE}`.")

if __name__ == "__main__":
    print("🔍 Iniciando transformação dos dados...")
    load_and_clean_data()
