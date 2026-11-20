# 🚀 Brazilian E-Commerce End-to-End ETL Pipeline 

> A robust, production-grade Data Engineering pipeline built to process, transform, and model the Olist Brazilian E-Commerce dataset (~100k orders) using modern Data Lakehouse & ELT patterns.

---

## 🏗️ System Architecture


The pipeline follows the **Medallion Architecture (Bronze $\rightarrow$ Silver $\rightarrow$ Gold)**, containerized via **Docker Compose**, orchestrated by **Apache Airflow**, and transformed using **dbt Core** inside a PostgreSQL Data Warehouse.

![Architecture Diagram](docs/architecture_diagram.png)

---
## 🛠️ Tech Stack & Tools

* **Orchestration:** Apache Airflow (Task scheduling & DAG management).
* **Storage (Data Lake):** MinIO (S3-compatible Object Storage for Raw data).
* **Database (Data Warehouse):** PostgreSQL[cite: 4, 5].
* **Transformation & Testing:** dbt Core (SQL-based modular transformations & data quality testing).
* **Environment:** Docker & Docker Compose (Containerized infrastructure).
* **Business Intelligence:** Microsoft Power BI.
* **Language:** Python.


---
## 🖥️ Pipeline Execution & BI Visualization

End-to-end verification of the data pipeline execution, data lineage, and business intelligence reporting:

### 1. Apache Airflow Orchestration
* **Interface:** `http://localhost:8080` — Automated daily scheduling and execution monitoring across ingestion, loading, dbt transformations, and data quality tests.

![Airflow DAG Success](docs/airflow_dag_success.png)

### 2. dbt Data Lineage & Documentation
* **Interface:** `http://localhost:8081` (`dbt docs serve`) — End-to-end dependency graph mapping raw sources through staging and intermediate layers into the final Star Schema marts.

![dbt Lineage Graph](docs/dbt_lineage.png)

### 3. Power BI Analytics Dashboard *(Coming Soon)*
* **Source:** Connected directly to PostgreSQL `gold_mart` / `03_marts` schema — Tracking revenue trends, delivery SLA performance, and customer RFM segmentation.

     UPDATING...

---

## 📁 Project Structure

```text
brazilian-ecommerce-pipeline/
├── config/
│   ├── settings.py                   # Centralized connection configs
│   └── logger.py                     # Standardized logging configuration for ETL scripts & pipeline monitoring
├── dags/                             # Apache Airflow DAG orchestrating the end-to-end workflow
│   └── airflow.py                    # Main DAG definition scheduling ingestion, loading, dbt tasks and tests
├── dashboard/                        # Power BI dashboard files & visualizations connected to `gold_mart`
├── data/
│   └── raw/                          # Raw Olist CSV files downloaded from Kaggle
├── dbt_olist_project/                # dbt Core project for modular SQL transformations & testing
│   ├── .dbt/                         # Local dbt profile connection configuration (profiles.yml)
│   ├── dbt_packages/                 # External dbt packages installed via `dbt deps` (e.g., dbt_utils)
│   ├── macros/                       # Reusable Jinja SQL functions & custom generic test definitions
│   ├── dbt_project.yml               # Project configuration, schema routing, and materialization settings
│   ├── models/
│   │   ├── 01_staging/               # Raw source definitions (_sources.yml), 1-to-1 standardized staging models & column 
|   |   |                               tests (stg_olist_*.sql / .yml)
│   │   ├── 02_intermediate/          # Pre-aggregated payments & translated product lookups (int_order_payments_aggregated, 
|   |   |                               int_products_english)
│   │   └── 03_marts/                 # Star Schema dimensions, fact tables & mart-level tests (dim_*, fact_*, schema.yml)
│   └── tests/                        # Singular SQL data quality tests
├── docs/                             # Architecture diagrams, Airflow & dbt execution screenshots for documentation
├── images/                           # Custom Dockerfiles extending base service images with project dependencies
│   ├── airflow/
│   │   └── Dockerfile                # Custom Airflow image 
│   └── jupyter/
│       └── Dockerfile                # Custom JupyterLab image 
├── notebooks/                        
├── scripts/
│   └── ingestion/
│       ├── ingest_minio.py           # Uploads csvs file to MinIO storage
│       ├── load_to_raw.py            # Read files from MinIO and loads into Postgres `raw` schema
│       └── init_postgres.sql         # Initializes raw schema & create tables
├── .env                              # Local environment variables & credentials 
├── .env.example                      # Template for required environment variables
├── docker-compose.yml                # Multi-container orchestration (PostgreSQL, MinIO, Airflow, Jupyter)
├── Makefile                          # Shortcut CLI commands for Docker setup
├── README.md                         # Comprehensive project documentation
└── requirements.txt                  # Python dependencies
```
---
## 🚀 Getting Started & Execution

Follow this step-by-step guide to install prerequisites, set up the environment, and run the end-to-end pipeline locally.

1. Environment Variables & dbt Profile
     1. Create .env from the template:
          cp .env.example .env
     Review .env and update credentials if needed (PostgreSQL user/password, MinIO root credentials, and Airflow admin credentials).

     2. Verify local dbt profiles.yml (for local dbt CLI execution):

     Ensure dbt_olist_project/.dbt/profiles.yml is configured to connect to PostgreSQL on localhost:5432 matching the credentials in your .env file.
     
2. Set Up Local Python Environment

5. Build & Start Infrastructure (Docker)
     Build the custom Docker images (images/airflow, images/jupyter) and spin up all services (PostgreSQL, MinIO, Apache Airflow, JupyterLab):
     ```text
     docker compose build --no-cache 
     docker compose up -d
     ```
7. Generate & View dbt Documentation & Lineage 
     ```text
     cd dbt_olist_project
     docker compose exec airflow-webserver dbt deps --project-dir /opt/airflow/dbt_olist_project --profiles-dir /opt/airflow/dbt_olist_project/.dbt

     docker compose exec airflow-webserver dbt docs generate --project-dir /opt/airflow/dbt_olist_project --profiles-dir /opt/airflow/dbt_olist_project/.dbt

     docker compose exec airflow-webserver dbt docs serve --project-dir /opt/airflow/dbt_olist_project --profiles-dir /opt/airflow/dbt_olist_project/.dbt --port 8081 --host 0.0.0.0
     ```
     Open http://localhost:8081 in your browser to explore model descriptions, column tests, and the full Lineage Graph.
     
6. Execute the End-to-End Pipeline
     1. Open the Apache Airflow UI at http://localhost:8080 and log in (default: admin / admin or check .env).
     2. Locate the brazilian_ecommerce_pipeline DAG, toggle it ON (Unpause), and click Trigger DAG.

7. Start the BI dashboard
     UPDATING...
--- 
## 📊 Data Modeling & Transformation Strategy

The project implements Dimensional Modeling (Kimball Methodology) inside the PostgreSQL Data Warehouse through three dbt layers:

     1. Staging Layer (stg_*): Direct tables over the raw schema. Handles data type casting, column standardizations and basic null filtering.

     2. Intermediate Layer (int_*): Modular SQL blocks joining staging models  to compute intermediate metrics.

     3. Marts Layer (dim_*, fct_*): Final business-ready star schema:

          Dimensions (dim_customers, dim_products, dim_sellers): Contextual attributes for filtering and grouping.

          Facts (fct_orders): Granular transactional metrics (freight value, delivery time, review scores) optimized for BI analytical queries.
---
## 🤝 Connect
👤 Author: [Hoang Vo Ba Huy](https://www.linkedin.com/in/huy-ho%C3%A0ng-v%C3%B5-b%C3%A1-6bab671a6/) | [GitHub](https://github.com/Huyhvb2505) 
     