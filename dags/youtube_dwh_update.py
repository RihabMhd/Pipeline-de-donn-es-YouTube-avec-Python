from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="youtube_dwh_update",
    start_date=datetime(2026, 9, 14),
    schedule='@daily',
    catchup=False,
    tags=["youtube", "dwh"],
) as dag:

    load_staging = BashOperator(
        task_id="load_staging",
        bash_command="python /opt/airflow/src/youtube/load_staging.py"
    )

    transform_core = BashOperator(
        task_id="transform_core",
        bash_command="python /opt/airflow/src/youtube/transform_core.py"
    )

    load_staging >> transform_core