import os
import requests
import polars as pl
from dotenv import load_dotenv

# Carregar credenciais do .env
load_dotenv()
IEEE_API_KEY = os.getenv("IEEE_API_KEY")

QUERY = "mobile applications AND health education AND data analysis"

def fetch_ieee_articles(query, max_results=10):
    """ Extrai artigos da API IEEE Xplore e retorna um DataFrame """
    url = "http://ieeexploreapi.ieee.org/api/v1/search/articles"
    params = {
        "apikey": IEEE_API_KEY,
        "format": "json",
        "max_records": max_results,
        "querytext": query,
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    if "articles" not in data:
        print("❌ Erro na resposta da API IEEE Xplore:", data)
        return pl.DataFrame()

    articles = []
    for article in data["articles"]:
        articles.append({
            "id": article.get("article_number", "N/A"),
            "title": article.get("title", "N/A"),
            "journal": article.get("publication_title", "N/A"),
            "authors": ", ".join(article.get("authors", [])) if "authors" in article else "N/A",
            "pub_date": article.get("publication_year", "N/A"),
            "source": "IEEE Xplore",
        })

    return pl.DataFrame(articles)

if __name__ == "__main__":
    print("🔍 Extraindo artigos do IEEE Xplore...")
    ieee_data = fetch_ieee_articles(QUERY)
    if ieee_data.is_empty():
        print("❌ Nenhum artigo retornado.")
    else:
        ieee_data.write_csv("../data/raw/ieee_articles.csv")
        print(f"✅ {len(ieee_data)} artigos salvos em `data/raw/ieee_articles.csv`.")
