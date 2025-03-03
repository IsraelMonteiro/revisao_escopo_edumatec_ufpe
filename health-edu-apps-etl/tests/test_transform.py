import polars as pl
from health_edu_apps_etl.transform_data import load_and_clean_data, OUTPUT_FILE

def test_transform_data():
    """ Testa a transformação dos dados """
    load_and_clean_data()
    
    # 📥 Carregar dados transformados
    df = pl.read_parquet(OUTPUT_FILE)
    
    # 🔹 Verificar se o arquivo foi criado
    assert df.shape[0] > 0, "❌ Erro: Nenhum artigo foi salvo!"
    
    # 🔹 Verificar se não há títulos duplicados
    assert df["title"].n_unique() == df.shape[0], "❌ Erro: Existem artigos duplicados!"

    # 🔹 Verificar se as datas estão no formato correto
    assert df["pub_date"].dtype == pl.Date, "❌ Erro: Datas não estão no formato YYYY-MM-DD!"

    print("✅ Teste de transformação passou!")

if __name__ == "__main__":
    test_transform_data()
