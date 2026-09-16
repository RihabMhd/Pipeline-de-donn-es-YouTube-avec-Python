from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def test_extraction():
    print("DAG 1 - Extraction started")


with DAG(
    dag_id="youtube_extraction",
    start_date=datetime(2026, 9, 14),
    schedule=None,
    catchup=False,
    tags=["youtube", "extraction"],
) as dag:

    extraction = PythonOperator(
        task_id="extraction",
        python_callable=test_extraction,
    )