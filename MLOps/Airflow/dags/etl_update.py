"""
DAG: etl_update

Concepts demonstrated:
- FileSensor as an external trigger
- Sequential ETL steps (cleanup → processing)
- Branching logic using BranchPythonOperator
- Conditional execution (refresh downstream data only on weekdays)
- Skipped tasks vs executed tasks
"""

from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta

# Business logic function (define here if not available as a module)
def process_data(**kwargs):
    print("Processing data...")  # Replace with actual processing logic


# -------------------------------------------------------------------
# Default DAG arguments
# -------------------------------------------------------------------
# start_date: when Airflow starts scheduling this DAG
# sla: alerts if a task takes longer than expected
default_args = {
    "start_date": datetime(2023, 1, 1),
    "sla": timedelta(minutes=90),
}

# -------------------------------------------------------------------
# DAG definition
# -------------------------------------------------------------------
dag = DAG(
    dag_id="etl_update",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
)

# -------------------------------------------------------------------
# 1. Sensor task
# -------------------------------------------------------------------
# Waits for an external file to appear.
# This simulates an upstream system signaling that new data is ready.
sensor = FileSensor(
    task_id="sense_file",
    filepath="/home/repl/workspace/startprocess.txt",
    poke_interval=45,      # check every 45 seconds
    mode="poke",           # block the worker while waiting
    dag=dag,
)

# -------------------------------------------------------------------
# 2. Cleanup task
# -------------------------------------------------------------------
# Removes leftover temporary files from previous runs.
# Typical first step in ETL pipelines to ensure idempotency.
cleanup_task = BashOperator(
    task_id="cleanup_tempfiles",
    bash_command="rm -f /home/repl/*.tmp",
    dag=dag,
)

# -------------------------------------------------------------------
# 3. Core processing task
# -------------------------------------------------------------------
# Executes the main data processing logic.
# provide_context=True is legacy (Airflow 1.x), but included here
# to show how runtime context (ds, execution_date, etc.) can be passed.
process_task = PythonOperator(
    task_id="run_processing",
    python_callable=process_data,
    provide_context=True,   # not required in Airflow 2.x, but harmless
    dag=dag,
)

# -------------------------------------------------------------------
# 4. Branching logic
# -------------------------------------------------------------------
# Decide whether to refresh downstream datasets.
# Rule:
# - Weekdays → refresh downstream data
# - Weekends → skip refresh (save resources)
def decide_refresh(**kwargs):
    execution_date = datetime.strptime(kwargs["execution_date"], "%Y-%m-%d")

    # weekday(): Monday=0 ... Sunday=6
    if execution_date.weekday() < 5:
        return "refresh_downstream_data"
    else:
        return "skip_refresh"


branch_task = BranchPythonOperator(
    task_id="decide_downstream_refresh",
    python_callable=decide_refresh,
    provide_context=True,
    dag=dag,
)

# -------------------------------------------------------------------
# 5. Downstream branch tasks
# -------------------------------------------------------------------
# Actual refresh of dependent datasets (e.g., aggregates, marts, caches)
refresh_task = PythonOperator(
    task_id="refresh_downstream_data",
    python_callable=lambda: print("Refreshing downstream datasets"),
    dag=dag,
)

# Dummy task used when refresh is intentionally skipped
skip_task = EmptyOperator(
    task_id="skip_refresh",
    dag=dag,
)

# -------------------------------------------------------------------
# Dependency graph (execution order)
# -------------------------------------------------------------------
# Sensor → Cleanup → Core Processing → Branch
# Branch → (Refresh OR Skip)
sensor >> cleanup_task >> process_task
process_task >> branch_task >> [refresh_task, skip_task]
