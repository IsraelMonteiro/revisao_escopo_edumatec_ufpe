from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging
import os
from health_edu_apps_etl.etl_pipeline import run_etl
from health_edu_apps_etl.generate_report import generate_report

# Configuração da DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 3, 2),
    "email_on_failure": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "etl_pipeline_articles",
    default_args=default_args,
    description="Pipeline ETL automatizado para extração e análise de artigos científicos",
    schedule_interval="0 6 * * *",  # Executa todos os dias às 06:00
    catchup=False,
)

# Tarefa 1: Executar o pipeline de ETL
def etl_task():
    logging.info("🚀 Iniciando ETL...")
    run_etl()

task_etl = PythonOperator(
    task_id="run_etl",
    python_callable=etl_task,
    dag=dag,
)

# Tarefa 2: Gerar Relatório
def generate_report_task():
    logging.info("📊 Gerando relatório de artigos...")
    generate_report()

task_generate_report = PythonOperator(
    task_id="generate_report",
    python_callable=generate_report_task,
    dag=dag,
)

# Dependências das tarefas
task_etl >> task_generate_report
