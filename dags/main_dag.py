from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 10),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    "crawler",
    default_args=default_args,
    description="Simple Crawler To Get Data",
    schedule_interval=timedelta(days=7),  # Set it to 7 days
    catchup=False
)


def run_bs_buy_crawler():
    
    command = "python ./web-scrapers/bs_buy_crawler.py"
    import subprocess

    subprocess.run(command, shell=True)


def run_bs_rent_crawler():
    command = "python ./web-scrapers/bs_rent_crawler.py"
    import subprocess

    subprocess.run(command, shell=True)


# Define tasks to run the crawlers using PythonOperator
run_bs_buy_crawler_task = PythonOperator(
    task_id='run_bs_buy_crawler_task',
    python_callable=run_bs_buy_crawler,
    dag=dag
)

run_bs_rent_crawler_task = PythonOperator(
    task_id='run_bs_rent_crawler_task',
    python_callable=run_bs_rent_crawler,
    dag=dag
)

# Set the task dependencies
run_bs_buy_crawler_task >> run_bs_rent_crawler_task
