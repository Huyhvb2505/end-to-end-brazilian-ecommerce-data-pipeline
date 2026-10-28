FROM apache/airflow:2.8.1-python3.10

USER root

# Cài đặt các gói hệ thống cơ bản
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

USER airflow

# Cài đặt Python packages
COPY requirements.txt /opt/airflow/
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt