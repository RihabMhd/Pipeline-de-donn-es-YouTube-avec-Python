from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator #allows Airflow to execute a command in the Airflow environment
from airflow.operators.trigger_dagrun import TriggerDagRunOperator


with DAG(
    dag_id="youtube_extraction",
    start_date=datetime(2026, 9, 14),
    schedule='@daily',
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

    trigger_dag2 = TriggerDagRunOperator(
        task_id="trigger_dwh_update",
        trigger_dag_id="youtube_dwh_update"
    )

    extraction >> get_details >> trigger_dag2