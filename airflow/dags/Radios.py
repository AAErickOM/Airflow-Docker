#!/usr/bin/env python
import os
import time
import logging
import requests
import pandas as pd

from datetime import datetime


from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

def scrap_radio(stream_url, label, factor=150, path="", delay=0):
    if not os.path.isdir(path):
        os.makedirs(path)

    logging.info(f"[{label}] 20 seg audio start downloading ...")

    try:
        r = requests.get(stream_url, stream=True)
        block = r.iter_content(1024 * factor)
        now = datetime.today().strftime("%Y%m%d%H%M%S")
        filename = f"/{label}_{now}.mp3"

        with open(path + filename, "wb") as file:
            file.write(block)

    except:
        pass

#Radios a ser scrapeadas
bdRadios = pd.read_csv("/usr/local/airflow/dags/Radios.csv")

#Creando DAG para Airflow


with DAG(
        'Radios',
        # These args will get passed on to each operator
        # You can override them on a per-task basis during operator initialization
        default_args={
            'depends_on_past': False,
            'email': ['eore@apoyoconsultoria.com'],
            'email_on_failure': False,
            'email_on_retry': False,
            'retries': 1,
            'retry_delay': timedelta(minutes=5),
            # 'queue': 'bash_queue',
            # 'pool': 'backfill',
            # 'priority_weight': 10,
            # 'end_date': datetime(2016, 1, 1),
            # 'wait_for_downstream': False,
            # 'sla': timedelta(hours=2),
            # 'execution_timeout': timedelta(seconds=300),
            # 'on_failure_callback': some_function,
            # 'on_success_callback': some_other_function,
            # 'on_retry_callback': another_function,
            # 'sla_miss_callback': yet_another_function,
            # 'trigger_rule': 'all_success'
        },
        description='Descarga de radios',
        schedule_interval=timedelta(seconds=20),
        start_date=datetime(2021, 1, 1),
        catchup=False,
        tags=["Radio"],
) as dag:
    run_scripts = DummyOperator(
        task_id="init",
        dag=dag
    )

    lista_procesos = []

    for radio in bdRadios.index:
        radio_url = bdRadios["url"][radio]
        radio_name = bdRadios["radio"][radio]
        radio_name = "_".join(radio_name.split())
        radio_factor = int(bdRadios["factor_descarga"][radio])
        stream = PythonOperator(
            task_id='Descarga_radio_{}'.format(radio_name),
            python_callable=scrap_radio,
            op_kwargs={"stream_url": radio_url,
                       "label": radio_name,
                       "factor": radio_factor,
                       "path": f"data/{radio_name}",
                       "delay": 10},
                dag=dag,)


