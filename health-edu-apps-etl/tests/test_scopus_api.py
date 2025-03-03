import os
import requests
import json
from dotenv import load_dotenv

# Carregar credenciais do .env
load_dotenv()
SCOPUS_API_KEY = os.getenv("SCOPUS_API_KEY")

# 🚀 Definir a consulta de teste
QUERY = "mobile applications AND health education AND data analysis"
API_URL = "https://api.elsevier.com/content/search/scopus"

def test_scopus_api():
    """ Teste para verificar se a API do Scopus está respondendo corretamente. """
    headers = {
        "X-ELS-APIKey": SCOPUS_API_KEY,
        "Accept": "application/json"
    }
    params = {
        "query": QUERY,
        "count": 5,  # Buscar apenas 5 artigos para teste
    }
    
    response = requests.get(API_URL, headers=headers, params=params)
    
    assert response.status_code == 200, f"❌ Erro: A API do Scopus não respondeu corretamente! Código: {response.status_code}"

    data = response.json()
    
    # Verificar se a resposta contém artigos
    assert "search-results" in data, "❌ Erro: 'search-results' não encontrado na resposta!"
    assert "entry" in data["search-results"], "❌ Erro: 'entry' não encontrado na resposta!"
    assert len(data["search-results"]["entry"]) > 0, "❌ Erro: Nenhum artigo retornado!"

    print(f"✅ Teste da API Scopus passou! Retornou {len(data['search-results']['entry'])} artigos.")

# 🚀 Executar o teste
if __name__ == "__main__":
    test_scopus_api()
