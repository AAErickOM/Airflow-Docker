FROM puckel/docker-airflow:1.10.9

COPY airflow/airflow.cfg ${AIRFLOW_HOME}/airflow.cfg

RUN mkdir -p data
