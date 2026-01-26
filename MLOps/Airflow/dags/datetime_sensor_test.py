from airflow import DAG
from airflow.sensors.date_time import DateTimeSensor
from datetime import datetime

with DAG(
    dag_id="datetime_sensor_test",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    wait_until_time = DateTimeSensor(
        task_id="wait_until_9am",
        target_time="2024-01-02T09:00:00",
        poke_interval=60,
        mode="reschedule",
    )
