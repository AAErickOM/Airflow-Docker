#!/usr/bin/env python
import os
import pandas as pd

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from scripts.procesos import scrap_radio
from scripts.leerymover import read_speech_basic
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
        description='Descarga de radios',
        schedule_interval=timedelta(seconds=20),
        start_date=datetime(2021, 1, 1),
        catchup=False,
        tags=["Radio"],
) as dag:



    for radio in bdRadios.index:
        radio_url = bdRadios["url"][radio]
        radio_name = bdRadios["radio"][radio]
        radio_name = "_".join(radio_name.split())
        radio_factor = int(bdRadios["factor_descarga"][radio])

        #Creando rutas
        ruta = f"data/{radio_name}"
        ruta_read = f"data/{radio_name}_read"
        ruta_transcript = f"data/{radio_name}_transcript"
        ruta_fail = f"data/{radio_name}_fail"

        if not os.path.isdir(ruta_read):
            os.makedirs(ruta_read)

        if not os.path.isdir(ruta_transcript):
            os.makedirs(ruta_transcript)

        if not os.path.isdir(ruta_fail):
            os.makedirs(ruta_fail)

        now = datetime.today().strftime("%Y%m%d%H%M%S")

        #Creacion de DAGs
        stream = PythonOperator(
            task_id='Descarga_radio_{}'.format(radio_name),
            python_callable=scrap_radio,
            op_kwargs={"stream_url": radio_url,
                       "now": now,
                       "label": radio_name,
                       "factor": radio_factor,
                       "path": f"data/{radio_name}",
                       "delay": 10},
            execution_timeout=timedelta(seconds = 30),
            dag=dag,)

        leerymover = PythonOperator(
            task_id='LeeryMover_{}'.format(radio_name),
            python_callable=read_speech_basic,
            op_kwargs={
                "path": ruta,
                "ruta_read":ruta_read,
                "ruta_transcript":ruta_transcript,
                "ruta_fail": ruta_fail,
            },
            execution_timeout=timedelta(seconds=30),
            dag=dag,)

        stream >> leerymover

        # Creando DAG para Airflow