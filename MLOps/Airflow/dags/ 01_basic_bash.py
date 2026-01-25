from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'zephyr',
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='basic_v1',
    default_args=default_args,
    description='Practice with BashOperator and dependencies',
    start_date=datetime(2026, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:
    
    task_1 = BashOperator(
        task_id='print_hello',
        bash_command='echo "Initializing ML Pipeline..."'
    )

    task_2 = BashOperator(
        task_id='create_temp_dir',
        bash_command='mkdir -p /tmp/airflow_practice'
    )

    # Task Dependency using the bitshift operator
    task_1 >> task_2