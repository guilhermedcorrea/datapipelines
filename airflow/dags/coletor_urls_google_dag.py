import lxml.html as parser
import requests
import csv
import time
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow import models
from airflow.models.baseoperator import chain
from datetime import datetime, timedelta
from selenium.webdriver.chrome.options import Options



def urls_sellers():
    pass


default_args = {
  'start_date': datetime(2022,8,31),
  'sla': timedelta(minutes=50)
}
    
with DAG('urls_google',  default_args=default_args,
   catchup=False) as dag:

    urls_sellers = PythonOperator(
        task_id = 'urls_google',
        python_callable = urls_sellers
    )

urls_sellers
