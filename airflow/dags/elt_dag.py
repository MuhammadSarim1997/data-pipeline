from datetime import datetime, timedelta
from airflow import DAG
from docker.types import Mount
from airflow.operators.python import PythonOperator
# from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
# from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.docker.operators.docker import DockerOperator
import subprocess
from Airbyte_conection import trigger_airbyte_sync

# connection_id = '3e15109e-9051-4f23-8442-3df8d8941bdc'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

 


# def run_elt_script():
#     script_path = '/opt/airflow/elt/elt_script.py'
    
#     result = subprocess.run(['python', script_path], capture_output=True,text=True)
#     if result.returncode != 0:
#         raise Exception(f"Script failed with error: {result.stderr}")

dag = DAG(
    'elt_and_dbt',
    default_args=default_args,
    description='An ELT wokflow with dbt',
    start_date=datetime(2025, 6, 19),
    catchup=False,
)


t1 = PythonOperator(
        task_id='trigger_airbyte_sync',
        python_callable=trigger_airbyte_sync,
        execution_timeout=timedelta(minutes=20),
        dag=dag,
    )

# t1 = AirbyteTriggerSyncOperator(
#     task_id='airbyte_postgres_postgress',
#     airbyte_conn_id='airbyte',
#     connection_id=connection_id,
#     asynchronous=False,
#     timeout=3600,
#     wait_seconds=5,
#     # python_callable=run_elt_script,
#     dag=dag,
# )

t2 = DockerOperator(
    task_id='dbt_run',
    image='ghcr.io/dbt-labs/dbt-postgres:1.4.7',
    command='run --profiles-dir /root --project-dir /opt/dbt',
    auto_remove=True,
    docker_url='unix://var/run/docker.sock',
    network_mode='elt_network',
    mounts=[
        Mount(source='/home/sarim/data-pipeline/custom_postgres', target='/opt/dbt', type='bind'),
        Mount(source='/home/sarim/.dbt', target='/root', type='bind'),
    ],
    dag=dag,
)

t1 >> t2