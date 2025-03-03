import streamlit as st
import pandas as pd
import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os

# 📌 Caminho do arquivo processado
processed_data_path = "data/processed/articles.parquet"

# 📌 Verificar se o arquivo existe
if not os.path.exists(processed_data_path):
    st.error(f"Arquivo {processed_data_path} não encontrado! Verifique a extração e transformação dos dados.")
    st.stop()

# 📌 Carregar os dados processados
df = pl.read_parquet(processed_data_path).to_pandas()

# 📊 Sidebar - Filtros
st.sidebar.header("Filtros")
bases_disponiveis = df["source"].unique()
bases_selecionadas = st.sidebar.multiselect("Filtrar por Base de Dados", bases_disponiveis, default=bases_disponiveis)
anos_disponiveis = sorted(df["pub_date"].dropna().astype(str).unique())
ano_selecionado = st.sidebar.selectbox("Filtrar por Ano", anos_disponiveis, index=len(anos_disponiveis)-1)

# 📊 Aplicar filtros
df_filtrado = df[(df["source"].isin(bases_selecionadas)) & (df["pub_date"].astype(str) == ano_selecionado)]

# 📊 Exibir métricas gerais
st.title("📚 Painel Interativo de Artigos Científicos")
st.write(f"**Total de Artigos no Filtro Atual:** {len(df_filtrado)}")

# 📊 Gráfico de Contagem por Base de Dados
st.subheader("Distribuição de Artigos por Base de Dados")
fig, ax = plt.subplots()
sns.countplot(y=df_filtrado["source"], order=df_filtrado["source"].value_counts().index, palette="viridis", ax=ax)
plt.xlabel("Quantidade de Artigos")
st.pyplot(fig)

# 📊 Nuvem de Palavras para Títulos
st.subheader("Nuvem de Palavras dos Títulos de Artigos")
text = " ".join(df_filtrado["title"].dropna())
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
fig, ax = plt.subplots()
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)

# 📊 Tabela de Artigos
st.subheader("📄 Lista de Artigos")
st.dataframe(df_filtrado[["title", "authors", "journal", "pub_date", "source"]].reset_index(drop=True))

# 📥 Exportação
def converter_para_csv(df):
    return df.to_csv(index=False).encode("utf-8")

csv = converter_para_csv(df_filtrado)
st.download_button("📥 Baixar Dados Filtrados", data=csv, file_name="artigos_filtrados.csv", mime="text/csv")

st.success("✅ Aplicação carregada com sucesso!")
