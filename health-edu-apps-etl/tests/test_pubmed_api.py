import os
import requests
import json
from dotenv import load_dotenv

# Carregar credenciais do .env
load_dotenv()
PUBMED_API_KEY = os.getenv("PUBMED_API_KEY")

# 🚀 Definir a consulta de teste
QUERY = '("mobile applications"[Title/Abstract] OR "health apps"[Title/Abstract]) AND ("data analysis"[Title/Abstract])'
API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

def test_pubmed_api():
    """ Teste para verificar se a API do PubMed está respondendo corretamente. """
    params = {
        "db": "pubmed",
        "term": QUERY,
        "retmax": 5,  # Buscar apenas 5 artigos para teste
        "retmode": "json",
        "api_key": PUBMED_API_KEY,
    }
    
    response = requests.get(API_URL, params=params)
    
    assert response.status_code == 200, "❌ Erro: A API do PubMed não respondeu corretamente!"
    
    data = response.json()
    assert "esearchresult" in data, "❌ Erro: 'esearchresult' não encontrado na resposta!"
    assert len(data["esearchresult"]["idlist"]) > 0, "❌ Erro: Nenhum artigo retornado!"

    print("✅ Teste da API PubMed passou! Retornou", len(data["esearchresult"]["idlist"]), "artigos.")

# 🚀 Executar o teste
if __name__ == "__main__":
    test_pubmed_api()
