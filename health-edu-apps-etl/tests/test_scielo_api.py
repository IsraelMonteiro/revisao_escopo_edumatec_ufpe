import os
import requests
import json
import time
from dotenv import load_dotenv

# 🔹 Carregar variáveis de ambiente
load_dotenv()

# 🔹 Configuração da API SciELO
BASE_URL = "http://articlemeta.scielo.org/api/v1/article/"
COLLECTION = "scl"

# 🔍 Lista de códigos de artigos para teste
ARTICLE_CODES = [
    "S0103-40142005000200002",
    "S0103-40142005000200003",
    "S0103-40142005000200004"
]

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

        except requests.JSONDecodeError:
            print(f"❌ Erro ao decodificar JSON para {article_code}")
            return None

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
        return "❌ Erro ao obter dados do artigo."

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

    return f"✅ {title} | {journal} | {authors} | {pub_date}"

def test_scielo_api():
    """Executa um teste de conexão e validação de artigos da SciELO."""
    print("\n🔍 **Iniciando teste da API SciELO...**\n")

    results = []
    for code in ARTICLE_CODES:
        article_data = fetch_scielo_article(code)

        # 🔹 Exibe JSON formatado para depuração (se necessário)
        # print(json.dumps(article_data, indent=2, ensure_ascii=False))

        if article_data:
            results.append(process_article_data(article_data))
        else:
            results.append(f"❌ Erro ao obter dados do artigo {code}")

    print("\n📋 **Resultados do Teste**\n")
    for res in results:
        print(res)

# 🚀 Executar o teste
if __name__ == "__main__":
    test_scielo_api()
