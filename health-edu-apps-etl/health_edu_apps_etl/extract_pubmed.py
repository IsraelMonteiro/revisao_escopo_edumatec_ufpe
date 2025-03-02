import os
import requests
import polars as pl
from dotenv import load_dotenv

# Carregar credenciais do .env
load_dotenv()
PUBMED_API_KEY = os.getenv("PUBMED_API_KEY")

QUERY = '("mobile applications"[Title/Abstract] OR "health apps"[Title/Abstract]) AND ("data analysis"[Title/Abstract])'

def fetch_pubmed_articles(query, max_results=10):
    """ Extrai artigos da API PubMed e retorna um DataFrame """
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "api_key": PUBMED_API_KEY,
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    if "esearchresult" not in data:
        print("❌ Erro na resposta da API PubMed:", data)
        return pl.DataFrame()

    article_ids = data["esearchresult"]["idlist"]
    articles = []

    for article_id in article_ids:
        article_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        article_params = {"db": "pubmed", "id": article_id, "retmode": "json"}
        article_response = requests.get(article_url, params=article_params)
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

    return pl.DataFrame(articles)

if __name__ == "__main__":
    print("🔍 Extraindo artigos da PubMed...")
    pubmed_data = fetch_pubmed_articles(QUERY)
    
    if pubmed_data.is_empty():
        print("❌ Nenhum artigo retornado.")
    else:
        # 📌 Garantir que o diretório "data/raw" existe
        output_dir = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
        os.makedirs(output_dir, exist_ok=True)  # Cria a pasta se não existir

        # 📌 Caminho correto do arquivo de saída
        output_file = os.path.join(output_dir, "pubmed_articles.csv")
        pubmed_data.write_csv(output_file)
        
        print(f"✅ {len(pubmed_data)} artigos salvos em `{output_file}`.")
