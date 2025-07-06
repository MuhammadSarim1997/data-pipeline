FROM apache/airflow:2.8.1

USER airflow

RUN pip install --no-cache-dir \
    apache-airflow-providers-docker \
    apache-airflow-providers-http \
    apache-airflow-providers-airbyte==2.1.4 \
    "apache-airflow-providers-openlineage>=1.8.0" \
    requests
    

USER root