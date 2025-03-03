
---

# **📊 Revisão de Escopo - EDUmatec UFPE**

**🛠 Projeto:** `health-edu-apps-etl`  
**📚 Objetivo:** Construção de um pipeline de ETL para **extração, transformação e análise de dados** sobre **aplicativos móveis para educação em saúde**, utilizando **IEEE Xplore, PubMed e outras bases acadêmicas**.

---

## **📌 Visão Geral**
Este projeto tem como foco a **coleta automatizada de artigos acadêmicos** sobre **aplicativos de saúde** para **educação preventiva**. O pipeline será implementado utilizando **tecnologias modernas para ETL**, garantindo:
- Extração otimizada de artigos das bases **IEEE Xplore, PubMed, Scopus, Web of Science, Google Scholar e SciELO**.
- Limpeza e transformação dos dados para análise estruturada.
- Armazenamento eficiente usando **Parquet e DuckDB**.
- Análise exploratória com **Streamlit** e **Machine Learning** para insights avançados.

---

## **🖥️ Tecnologias Utilizadas**
- **Python** → Processamento e análise de dados
- **Polars & Pandas** → Manipulação eficiente de grandes datasets
- **Apache Airflow** → Orquestração do pipeline de ETL
- **DuckDB** → Consultas SQL-like rápidas sem necessidade de um banco externo
- **PyArrow** → Suporte ao formato **Parquet**
- **BeautifulSoup & Requests** → Web Scraping (caso APIs estejam indisponíveis)
- **Streamlit** → Interface gráfica para análise interativa
- **OpenPyXL & ReportLab** → Exportação de dados para Excel e PDF

---

## **📂 Estrutura do Projeto**
```
health-edu-apps-etl/
├── health_edu_apps_etl/    # 📌 Módulo principal
│   ├── __init__.py
│   ├── config.py           # Configuração global
│   ├── etl_pipeline.py     # Orquestração do pipeline completo
│   ├── extract_pubmed.py   # Extração específica da PubMed
│   ├── extract_ieee.py     # Extração específica do IEEE Xplore
│   ├── extract_scopus.py   # Extração específica do Scopus
│   ├── extract_wos.py      # Extração específica do Web of Science
│   ├── extract_scholar.py  # Extração específica do Google Scholar
│   ├── extract_scielo.py   # Extração específica do SciELO
│   ├── transform_data.py   # Processamento e limpeza de dados
│   ├── utils.py            # Funções auxiliares
│
├── data/                   # 📂 Diretório para armazenar os dados
│   ├── raw/                # Dados brutos extraídos das fontes
│   ├── processed/          # Dados tratados e organizados
│   ├── articles.parquet    # Dados salvos no formato otimizado
│   ├── articles.csv        # Dados exportados para fácil visualização
│
├── notebooks/              # 📂 Notebooks para exploração de dados
│   ├── exploratory_analysis.ipynb
│
├── tests/                  # 📂 Testes automatizados
│   ├── __init__.py
│   ├── test_pubmed_api.py  # Teste da API PubMed
│   ├── test_ieee_api.py    # Teste da API IEEE Xplore
│   ├── test_extract.py     # Testes gerais de extração
│   ├── test_transform.py   # Testes de transformação
│
├── .env.example            # Exemplo de configuração de credenciais
├── .gitignore              # Arquivos ignorados pelo Git
├── pyproject.toml          # Configuração do Poetry
├── README.md               # Documentação principal

```

---

## **🚀 Como Rodar o Projeto**
### **1️⃣ Clonar o Repositório**
```bash
git clone https://github.com/IsraelMonteiro/revisao_escopo_edumatec_ufpe.git
cd revisao_escopo_edumatec_ufpe
```

### **2️⃣ Criar Ambiente Virtual**
**Se estiver usando `Poetry` (recomendado):**
```bash
poetry install
```
**Ou com `venv` e `pip`:**
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### **3️⃣ Configurar as Chaves de API**
Crie um arquivo `.env` e adicione suas chaves:
```
PUBMED_API_KEY=seu_token_aqui
IEEE_API_KEY=seu_token_aqui
```

### **4️⃣ Executar a Extração de Dados**
```bash
python health-edu-apps-etl/health_edu_apps_etl/extract_articles.py
```

### **5️⃣ Rodar a Interface Streamlit**
```bash
streamlit run health-edu-apps-etl/health_edu_apps_etl/analyze_data.py
```

---

## **🔍 Próximos Passos**
✅ Implementar a extração de dados via APIs (PubMed & IEEE Xplore)  
✅ Criar pipeline de limpeza e transformação de dados  
🔄 Estruturar análise e visualização interativa  
🚀 Automatizar todo o processo com Apache Airflow  

---

## **🤝 Contribuições**
Caso tenha sugestões ou queira contribuir com o projeto, sinta-se à vontade para abrir **issues** ou **pull requests**.  

---

## **📜 Licença**
Este projeto é open-source sob a licença **MIT**.

---


