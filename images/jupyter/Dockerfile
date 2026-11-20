FROM jupyter/scipy-notebook:latest

USER root

RUN pip install --no-cache-dir \
    boto3 \
    minio \
    pyarrow \
    "SQLAlchemy<2.0.0" \
    psycopg2-binary \
    python-dotenv

USER ${NB_UID}
WORKDIR /home/jovyan/work