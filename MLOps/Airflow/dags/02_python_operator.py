from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator

def greet(name, age):
    print(f"Hello {name}, age {age}")
python_task = PythonOperator(
    task_id="greet_task",
    python_callable=greet,
    op_args=["Geoffery"], # positional arguments
    op_kwargs={"age": 25} # keyword arguments
)

email_task = EmailOperator(
    task_id="send_email",
    to="example@email.com",
    subject="Airflow Task Completed",
    html_content="<h3>Task finished successfully</h3>"
)