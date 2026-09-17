from datetime import datetime

import importlib


airflow = importlib.import_module("airflow")
PythonOperator = importlib.import_module("airflow.operators.python").PythonOperator
BashOperator = importlib.import_module("airflow.operators.bash").BashOperator
bash_command="python /opt/airflow/src/youtube/get_playlist.py"

with airflow.DAG(
    dag_id="youtube_extraction",
    start_date=datetime(2026, 9, 14),
    schedule=None,
    catchup=False,
    tags=["youtube", "extraction"],
) as dag:

    extraction = BashOperator(
    task_id="extract_playlist",
    bash_command="python /opt/airflow/src/youtube/get_playlist.py"
)

    get_details = BashOperator(
        task_id="get_video_details",
        bash_command="python /opt/airflow/src/youtube/get_video_details.py"
    )

    extraction >> get_details