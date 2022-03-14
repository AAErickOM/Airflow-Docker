

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from pysentimiento import create_analyzer





def prueba(text):
    analyzer = create_analyzer(task="sentiment", lang="es")
    print(analyzer.predict(text))

#Creando DAG para Airflow

with DAG(
        'Prueba',
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
        description='Prueba',
        schedule_interval=timedelta(seconds=20),
        start_date=datetime(2021, 1, 1),
        catchup=False,
        tags=["Radio"],
) as dag:
    PythonOperator(
        task_id='Prueba',
        python_callable=prueba,
        op_kwargs={"text": "Pesimo servicio, horrible experiencia"},
        execution_timeout=timedelta(seconds=60),
        dag=dag, )