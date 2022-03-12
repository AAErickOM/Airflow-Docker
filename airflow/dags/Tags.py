#!/usr/bin/env python
import pandas as pd

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from scripts.tag import tag_file
#Radios a ser scrapeadas
bdRadios = pd.read_csv("/usr/local/airflow/dags/Radios.csv")

#Creando DAG para Airflow

with DAG(
        'AsignacionTags',
        # These args will get passed on to each operator
        # You can override them on a per-task basis during operator initialization
        default_args={
            'depends_on_past': False,
            'email': ['eore@apoyoconsultoria.com'],
            'email_on_failure': False,
            'email_on_retry': False,
            'retries': 1,
            'retry_delay': timedelta(seconds=1),
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
        description='Se asignan los tags de los textos',
        schedule_interval=timedelta(seconds=60),
        start_date=datetime(2021, 1, 1),
        catchup=False,
        tags=["Radio"],
) as dag:

    for radio in bdRadios.index:
        radio_url = bdRadios["url"][radio]
        radio_name = bdRadios["radio"][radio]
        radio_name = "_".join(radio_name.split())
        radio_factor = int(bdRadios["factor_descarga"][radio])

        tags = PythonOperator(
            task_id='Tags_{}'.format(radio_name),
            python_callable=tag_file,
            op_kwargs={"radio": radio_name},
            execution_timeout=timedelta(seconds=60),
            dag=dag, )