from datetime import datetime, time,timedelta
from airflow.decorators import dag,task
from airflow.operators.bash import BashOperator
from scripts.ingest_minio import run_ingest_pipeline
from scripts.load_to_raw import run_load_pipeline


default_args = {
    'owner': 'Huy_De',
    'retries': 3,
    'retry_delay': timedelta(minutes=2)
}


@dag(
    dag_id='brazilian_ecommerce_pipeline',
    default_args=default_args,
    description='End-to-end pipeline process data',
    schedule_interval='@daily',
    start_date=datetime(2026, 11, 15),
    catchup=False
)

#create 2 tasks for 2 phases project
#1. process data raw ->minio -> postgres(raw schema) @task
#2. flow process data by dbt (staging -> intermediate ->marts ->dashboard) -> Bashoperator
#3. connect all tasks taska >> taskb v....v.v..

def brazilian_ecommerce_pipeline():
    @task
    def run_ingestion():
        run_ingest_pipeline() 
        return "Ingestion complete"

    @task
    def run_loading():
        run_load_pipeline()
        return "Loading complete"

    @task.bash
    def run_dbt_stg():
        return "cd /opt/airflow/dbt_olist_project && dbt run --select 01_staging"
    
    ingestion_task = run_ingestion()
    dbt_task = run_dbt()
    ingestion_task >> dbt_task
    
brazilian_ecommerce_pipeline_dag = brazilian_ecommerce_pipeline()
