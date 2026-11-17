from datetime import datetime,timedelta
from airflow.decorators import dag,task
from airflow.operators.bash import BashOperator
from scripts.ingest_minio import run_ingest_pipeline
from scripts.load_to_raw import run_load_pipeline


default_args = {
    'owner': 'Huy_De',
    'retries': 3,
    'retry_delay': timedelta(minutes=2),
    'execution_timeout': timedelta(hours=1) 
}


@dag(
    dag_id='brazilian_ecommerce_pipeline',
    default_args=default_args,
    description='End-to-end pipeline process data',
    schedule='@daily',
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
        

    @task
    def run_loading():
        run_load_pipeline()
        

    run_dbt_stg = BashOperator(
        task_id='run_dbt_stg',
        bash_command="cd /opt/airflow/dbt_olist_project && dbt run --select 01_staging --profiles-dir ./.dbt"
    )

    test_dbt_stg = BashOperator(
        task_id='test_dbt_stg',
        bash_command="cd /opt/airflow/dbt_olist_project && dbt test --select 01_staging --profiles-dir ./.dbt"
    )

    run_dbt_int = BashOperator(
        task_id='run_dbt_int',
        bash_command="cd /opt/airflow/dbt_olist_project && dbt run --select 02_intermediate --profiles-dir ./.dbt"
    )

    test_dbt_int = BashOperator(
        task_id='test_dbt_int',
        bash_command="cd /opt/airflow/dbt_olist_project && dbt test --select 02_intermediate --profiles-dir ./.dbt"
    )

    run_dbt_marts = BashOperator(
        task_id='run_dbt_marts',
        bash_command="cd /opt/airflow/dbt_olist_project && dbt run --select 03_marts --profiles-dir ./.dbt"
    )

    test_dbt_marts = BashOperator(
        task_id='test_dbt_marts',
        bash_command="cd /opt/airflow/dbt_olist_project && dbt test --select 03_marts --profiles-dir ./.dbt"
    )

    ingestion_task = run_ingestion()
    load_task = run_loading()
    

    ingestion_task >> load_task >> run_dbt_stg >> test_dbt_stg >> run_dbt_int >> test_dbt_int >> run_dbt_marts >> test_dbt_marts

brazilian_ecommerce_pipeline_dag = brazilian_ecommerce_pipeline()
