FROM puckel/docker-airflow:1.10.9

COPY airflow/airflow.cfg ${AIRFLOW_HOME}/airflow.cfg

COPY requirements.txt /requirements.txt
COPY preimport.py /preimport.py

USER root
RUN apt-get -y update
RUN apt-get install -y ffmpeg

USER airflow
RUN pip install -r /requirements.txt
RUN mkdir -p data
RUN python -m nltk.downloader stopwords
RUN python /preimport.py