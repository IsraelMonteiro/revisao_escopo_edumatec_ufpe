import os
import polars as pl
import pandas as pd
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from jinja2 import Environment, FileSystemLoader

# 📌 Caminhos de entrada e saída
DATA_PATH = "data/processed/articles.parquet"
OUTPUT_DIR = "reports"
PDF_FILE = os.path.join(OUTPUT_DIR, "articles_report.pdf")
HTML_FILE = os.path.join(OUTPUT_DIR, "articles_report.html")

# 📌 Criar diretório de saída, se necessário
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 📌 Carregar dados processados
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"❌ Arquivo de dados não encontrado: {DATA_PATH}")

df = pl.read_parquet(DATA_PATH).to_pandas()

# 📊 **1. Estatísticas Gerais**
stats = {
    "Total de artigos": len(df),
    "Bases de dados únicas": df["source"].nunique(),
    "Periódicos únicos": df["journal"].nunique(),
    "Autores únicos": df["authors"].nunique(),
}

# 📊 **2. Geração de Relatório em PDF**
def generate_pdf(file_path):
    c = canvas.Canvas(file_path, pagesize=landscape(letter))
    c.setFont("Helvetica-Bold", 16)
    c.drawString(30, 550, "📄 Relatório de Artigos Científicos")

    c.setFont("Helvetica", 12)
    y_position = 520
    for key, value in stats.items():
        c.drawString(30, y_position, f"{key}: {value}")
        y_position -= 20

    # Adicionar lista de artigos (apenas os primeiros 10 para evitar sobrecarga)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, y_position - 20, "📚 Lista de Artigos:")
    c.setFont("Helvetica", 10)
    y_position -= 40

    for index, row in df.head(10).iterrows():
        c.drawString(30, y_position, f"{index + 1}. {row['title']} - {row['authors']} ({row['source']})")
        y_position -= 20
        if y_position < 50:
            c.showPage()
            y_position = 550

    c.save()
    print(f"✅ Relatório PDF gerado: {file_path}")

# 📊 **3. Geração de Relatório em HTML**
def generate_html(file_path):
    env = Environment(loader=FileSystemLoader("."))
    template = env.from_string("""
    <html>
    <head>
        <title>Relatório de Artigos Científicos</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            h1 { color: #333; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1>📄 Relatório de Artigos Científicos</h1>
        <h2>📊 Estatísticas Gerais</h2>
        <ul>
            {% for key, value in stats.items() %}
                <li><strong>{{ key }}:</strong> {{ value }}</li>
            {% endfor %}
        </ul>
        
        <h2>📚 Lista de Artigos</h2>
        <table>
            <tr>
                <th>#</th>
                <th>Título</th>
                <th>Autores</th>
                <th>Fonte</th>
            </tr>
            {% for index, row in articles.iterrows() %}
            <tr>
                <td>{{ index + 1 }}</td>
                <td>{{ row['title'] }}</td>
                <td>{{ row['authors'] }}</td>
                <td>{{ row['source'] }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """)

    html_content = template.render(stats=stats, articles=df.head(10))
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ Relatório HTML gerado: {file_path}")

# 🚀 **Executar geração dos relatórios**
if __name__ == "__main__":
    generate_pdf(PDF_FILE)
    generate_html(HTML_FILE)
