import streamlit as st
import polars as pl
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 📌 Configuração da página no Streamlit
st.set_page_config(page_title="Dashboard de Artigos", layout="wide")

# 📌 Caminho do arquivo processado
processed_data_path = "data/processed/articles.parquet"

# 📌 Verificar se o arquivo existe
if not os.path.exists(processed_data_path):
    st.error(f"Arquivo {processed_data_path} não encontrado!")
    st.stop()

# 📌 Carregar os dados processados
df = pl.read_parquet(processed_data_path).to_pandas()

# 📊 Criar filtros interativos
st.sidebar.header("🔍 Filtros")
bases_disponiveis = df["source"].unique()
selected_base = st.sidebar.multiselect("Filtrar por Base de Dados", bases_disponiveis, default=bases_disponiveis)

anos_disponiveis = sorted(df["pub_date"].dropna().astype(str).unique())
selected_anos = st.sidebar.multiselect("Filtrar por Ano de Publicação", anos_disponiveis, default=anos_disponiveis)

# 📌 Aplicar filtros
df_filtered = df[(df["source"].isin(selected_base)) & (df["pub_date"].astype(str).isin(selected_anos))]

# 📊 Estatísticas gerais
st.header("📊 Estatísticas Gerais")
col1, col2, col3 = st.columns(3)
col1.metric("Total de Artigos", len(df_filtered))
col2.metric("Bases de Dados", df_filtered["source"].nunique())
col3.metric("Periódicos Únicos", df_filtered["journal"].nunique())

# 📊 Gráfico: Distribuição por Base de Dados
st.subheader("📌 Distribuição de Artigos por Base de Dados")
fig, ax = plt.subplots(figsize=(10, 5))
sns.countplot(y=df_filtered["source"], order=df_filtered["source"].value_counts().index, palette="viridis", ax=ax)
ax.set_xlabel("Quantidade de Artigos")
ax.set_ylabel("Base de Dados")
ax.set_title("Distribuição de Artigos por Base de Dados")
st.pyplot(fig)

# 📊 Gráfico: Distribuição ao longo do tempo
st.subheader("📌 Distribuição dos Artigos ao Longo do Tempo")
df_filtered["Ano"] = pd.to_datetime(df_filtered["pub_date"], errors="coerce").dt.year
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(df_filtered["Ano"].dropna(), bins=15, kde=True, color="blue", ax=ax)
ax.set_xlabel("Ano de Publicação")
ax.set_ylabel("Quantidade de Artigos")
ax.set_title("Distribuição dos Artigos ao Longo do Tempo")
st.pyplot(fig)

# 📊 Top 10 Periódicos
st.subheader("📌 Top 10 Periódicos")
top_journals = df_filtered["journal"].value_counts().head(10)
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=top_journals.values, y=top_journals.index, palette="magma", ax=ax)
ax.set_xlabel("Quantidade de Artigos")
ax.set_ylabel("Periódico")
ax.set_title("Top 10 Periódicos com Mais Artigos Publicados")
st.pyplot(fig)

# 📋 Exibir tabela interativa
st.subheader("📋 Tabela de Artigos")
st.dataframe(df_filtered, use_container_width=True)

# 📥 Download dos dados filtrados
st.subheader("📥 Exportar Dados")
excel_file = df_filtered.to_csv(index=False).encode("utf-8")
st.download_button(label="📥 Baixar CSV", data=excel_file, file_name="artigos_filtrados.csv", mime="text/csv")

st.success("✅ Análise concluída!")
