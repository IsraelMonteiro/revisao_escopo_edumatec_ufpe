import os
import requests
import json
import polars as pl
from dotenv import load_dotenv

# Carregar credenciais do arquivo .env
load_dotenv()
PUBMED_API_KEY = os.getenv("PUBMED_API_KEY")

# Termos de busca (reduzido para teste)
QUERY = '("mobile applications"[Title/Abstract] OR "health apps"[Title/Abstract]) AND ("data analysis"[Title/Abstract])'

def fetch_pubmed_articles(query, max_results=10):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "api_key": PUBMED_API_KEY,
    }
    
    response = requests.get(url, params=params)
    
    # 🚨 Depuração: Verificar resposta da API antes de tentar acessar "esearchresult"
    try:
        data = response.json()
    except json.JSONDecodeError:
        print("❌ Erro ao decodificar JSON! Resposta da API:", response.text)
        return pl.DataFrame()

    # 🚨 Verificar se "esearchresult" está presente na resposta
    if "esearchresult" not in data:
        print("❌ A resposta da API não contém 'esearchresult'. Resposta completa:", data)
        return pl.DataFrame()

    # Buscar detalhes dos artigos
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


# 🚀 Testar a função
if __name__ == "__main__":
    print("🔍 Testando extração da PubMed...")
    pubmed_data = fetch_pubmed_articles(QUERY)

    if pubmed_data.is_empty():
        print("❌ Nenhum dado retornado! Verifique a resposta da API.")
    else:
        print(f"✅ Extração bem-sucedida! {len(pubmed_data)} artigos coletados.")
