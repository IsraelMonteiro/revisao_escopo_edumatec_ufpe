import os
import requests
import json
from dotenv import load_dotenv

# Carregar credenciais do .env
load_dotenv()
IEEE_API_KEY = os.getenv("IEEE_API_KEY")

# 🚀 Definir a consulta de teste
QUERY = "mobile applications AND health education AND data analysis"
API_URL = "http://ieeexploreapi.ieee.org/api/v1/search/articles"

def test_ieee_api():
    """ Teste para verificar se a API do IEEE Xplore está respondendo corretamente. """
    params = {
        "apikey": IEEE_API_KEY,
        "format": "json",
        "max_records": 5,
        "querytext": QUERY,
    }
    
    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()  # Lança um erro se a resposta não for 200
        data = response.json()
        print(f"✅ Resposta da API IEEE: {json.dumps(data, indent=2)}")

        assert "articles" in data, "❌ Erro: 'articles' não encontrado na resposta!"
        assert len(data["articles"]) > 0, "❌ Erro: Nenhum artigo retornado!"

        print("✅ Teste da API IEEE Xplore passou! Retornou", len(data["articles"]), "artigos.")

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")
        print(f"🔍 Código de status: {response.status_code} - Resposta: {response.text}")

# 🚀 Executar o teste
if __name__ == "__main__":
    test_ieee_api()
