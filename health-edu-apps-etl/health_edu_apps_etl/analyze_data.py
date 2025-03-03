import os
import polars as pl
import pandas as pd
import logging
from collections import Counter
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv

# 🔹 Configuração de logs
logging.basicConfig(
    filename="analyze_data.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# 🔹 Carregar variáveis de ambiente
load_dotenv()

# 🔹 Diretórios e arquivos
BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
PROCESSED_FILE = PROCESSED_DATA_DIR / "all_articles.parquet"

# 🔹 Verificar se o arquivo existe
if not PROCESSED_FILE.exists():
    logging.error(f"❌ Arquivo {PROCESSED_FILE} não encontrado!")
    raise FileNotFoundError(f"Arquivo {PROCESSED_FILE} não encontrado!")

# 🔹 Carregar dados
df = pl.read_parquet(PROCESSED_FILE)

# 🔹 Converter para Pandas para facilitar visualizações
df_pd = df.to_pandas()

# 🔹 Estatísticas básicas
stats = {
    "Total de artigos": len(df_pd),
    "Bases de dados únicas": df_pd["source"].nunique(),
    "Periódicos únicos": df_pd["journal"].nunique(),
    "Autores únicos": df_pd["authors"].nunique(),
}

# 🔹 Contagem de artigos por base de dados
base_counts = df_pd["source"].value_counts()

# 🔹 Distribuição de artigos por ano
df_pd["pub_date"] = pd.to_datetime(df_pd["pub_date"], errors="coerce")
df_pd["Ano"] = df_pd["pub_date"].dt.year
yearly_counts = df_pd["Ano"].value_counts().sort_index()

# 🔹 Principais periódicos onde os artigos foram publicados
top_journals = df_pd["journal"].value_counts().head(10)

# 🔹 Frequência dos autores mais citados
author_list = df_pd["authors"].dropna().str.split(", ")
all_authors = [author for sublist in author_list.dropna() for author in sublist]
top_authors = Counter(all_authors).most_common(10)

# 🔹 Gerar gráficos 📊

def plot_bar(data, title, xlabel, ylabel, color="blue"):
    plt.figure(figsize=(10, 5))
    sns.barplot(x=data.values, y=data.index, palette=color)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()

# 📊 Número de artigos por base de dados
plot_bar(base_counts, "Quantidade de Artigos por Base de Dados", "Quantidade", "Base de Dados")

# 📊 Distribuição ao longo do tempo
plt.figure(figsize=(10, 5))
sns.lineplot(x=yearly_counts.index, y=yearly_counts.values, marker="o", color="red")
plt.xlabel("Ano de Publicação")
plt.ylabel("Quantidade de Artigos")
plt.title("Distribuição dos Artigos ao Longo do Tempo")
plt.grid()
plt.show()

# 📊 Top 10 Periódicos
plot_bar(top_journals, "Top 10 Periódicos com Mais Artigos", "Quantidade", "Periódico", color="magma")

# 📊 Top 10 Autores
top_authors_df = pd.DataFrame(top_authors, columns=["Autor", "Quantidade"])
plot_bar(top_authors_df.set_index("Autor"), "Top 10 Autores Mais Citados", "Quantidade", "Autor", color="green")

# 🔹 Converter estatísticas para DataFrame
stats_df = pd.DataFrame(list(stats.items()), columns=["Métrica", "Valor"])

print("\n📊 Estatísticas Gerais dos Artigos:")
print(stats_df.to_markdown(index=False))  # Exibe a tabela formatada no terminal

