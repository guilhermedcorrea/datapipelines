from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow import models
from airflow.models.baseoperator import chain
from datetime import datetime, timedelta




def insert_dw():
    pass


default_args = {
  'start_date': datetime(2022,8,31),
  'sla': timedelta(minutes=50)
}
    
with DAG('insert_dw',  default_args=default_args,
   catchup=False) as dag:

    madeira = PythonOperator(
        task_id = 'insert_dw',
        python_callable = insert_dw
    )

insert_dw
