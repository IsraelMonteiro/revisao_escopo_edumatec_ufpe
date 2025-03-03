import os
import pytest
from pathlib import Path
from health_edu_apps_etl.generate_report import generate_pdf, generate_html

# 📌 Diretório onde os relatórios são gerados
OUTPUT_DIR = Path("reports")
PDF_FILE = OUTPUT_DIR / "articles_report.pdf"
HTML_FILE = OUTPUT_DIR / "articles_report.html"

@pytest.fixture(scope="module")
def setup_directories():
    """Garante que o diretório de saída exista antes dos testes"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def test_generate_pdf(setup_directories):
    """Testa se o relatório em PDF é gerado corretamente"""
    generate_pdf(PDF_FILE)
    assert PDF_FILE.exists(), "❌ O relatório PDF não foi gerado corretamente!"

def test_generate_html(setup_directories):
    """Testa se o relatório em HTML é gerado corretamente"""
    generate_html(HTML_FILE)
    assert HTML_FILE.exists(), "❌ O relatório HTML não foi gerado corretamente!"

if __name__ == "__main__":
    pytest.main()
