from airflow import DAG  
from datetime import datetime, timedelta 
from airflow.operators.bash import BashOperator 

default_args = {
    'owner': 'airflow', 
	'depends_on_past' : 'False', 
	'start_date': datetime(2023,5,10),
	'retries': 1, 
	'retry_delay': timedelta(minutes=5)
}


dag  = DAG( 
    "crawler", 
    default_args = default_args, 
    description = "Simple Crawler To Get Data", 
    schedule = timedelta(days=1),
    catchup = False
) 

t1 = BashOperator( 
    task_id = "run_crawler",  
    bash_command = "./scripts/bs_rent_crawler.py",
    dag = dag
                ) 
t2 = BashOperator( 
    task_id = "clean_data",  
    bash_command = "./scripts/clean_rent_data.py",
    dag = dag
                )

t1 >>  t2