# 🚀 Brazilian E-Commerce End-to-End Data Pipeline (Medallion Architecture)

An end-to-end, production-style Batch ELT Data Engineering Pipeline built on the Brazilian E-Commerce Public Dataset by Olist (100,000+ orders across 9 normalized OLTP tables).

This project implements the Medallion Architecture (Bronze → Silver → Gold) using Python, Apache Airflow, MinIO (S3-Compatible Object Storage), PostgreSQL, dbt Core, Docker, and Power BI to transform raw transactional records into an analytics-ready Star Schema Data Warehouse and executive BI dashboards.

---

## 🏗️ Architecture


    [9 CSV Olist] 
     │ (1. Python + Pandas/PyArrow + boto3)
     ▼
[Tầng BRONZE — MinIO Data Lake] (Lưu file nén cột .parquet tại s3://olist-bronze/YYYY-MM-DD/)
     │ (2. Python SQLAlchemy / COPY)
     ▼
[PostgreSQL: Schema `raw`] (9 bảng thô nguyên bản từ Parquet nạp vào DB)
     │ (3. dbt Core: dbt snapshot + dbt run + dbt test)
     ▼
[Tầng SILVER — PostgreSQL: Schema `silver_dwh`] (Mô hình Star Schema: 1 Fact + 4 Dims, SCD Type 2, Index/Partition)
     │ (4. dbt Core: CTEs + Window Functions)
     ▼
[Tầng GOLD — PostgreSQL: Schema `gold_mart`] (3 bảng Mart tổng hợp sẵn chỉ số kinh doanh)
     │ (5. Direct Connection)
     ▼
[Power BI Dashboard] (Báo cáo Doanh thu, Giao vận SLA & Phân nhóm RFM)

## ✨ Tính năng nổi bật
* **Idempotent Upsert:** Xử lý dữ liệu trùng lặp, đảm bảo không bị nhân bản dữ liệu khi chạy lại pipeline.
* **Dead-Letter Queue (DLQ):** Tự động cách ly các bản ghi lỗi định dạng để xử lý sau mà không làm sập toàn bộ luồng.
* **Schema Validation:** Kiểm tra tính hợp lệ của kiểu dữ liệu đầu vào bằng Pydantic/Pandas trước khi lưu trữ.

## 🛠️ Tech stack
* **Data Lake Storage:** MinIO + Apache Parquet
* **Orchestration:** Apache Airflow 
* **Data Warehouse:** PostgreSQL
* **Data Transformation:** dbt Core
* **Business Intelligence:** Microsoft Power BI
* **Containerization:** Docker & Docker Compose

## 📁 Cấu trúc thư mục

├── config/
│   └── settings.py                   # Centralized MinIO (boto3) & PostgreSQL (SQLAlchemy) connection configs
├── data/
│   └── raw/                          # Raw Olist CSV files downloaded from Kaggle
├── scripts/
│   └── ingestion/
│       ├── upload_to_minio.py        # Step 1: Converts raw CSVs to Parquet and uploads to MinIO (Bronze)
│       └── load_minio_to_postgres.py # Step 2: Reads Parquet from MinIO and loads into Postgres `raw` schema
├── sql/
│   └── init_postgres.sql             # Initializes database schemas: `raw`, `silver_dwh`, `gold_mart`
├── olist_dbt/                        # Step 3: dbt Core project for Silver & Gold transformations
│   ├── dbt_project.yml
│   ├── snapshots/                    # SCD Type 2 snapshots (scd_customers.sql, scd_sellers.sql)
│   └── models/
│       ├── staging/                  # Source definitions and light column casting
│       ├── silver_dwh/               # Star Schema models (fact_order_items.sql, dim_*.sql, schema.yml)
│       └── gold_mart/                # Business Data Marts (mart_daily_sales.sql, mart_delivery_sla.sql,               mart_customer_rfm.sql)
├── dags/
│   └── olist_medallion_dag.py        # Step 4: Apache Airflow DAG orchestrating the end-to-end workflow
├── dashboard/
│   └── olist_executive_report.pbix   # Step 5: Power BI dashboard connected to `gold_mart`
├── docs/
│   └── images/                       # Architecture diagrams, Airflow DAG runs, EXPLAIN ANALYZE & BI screenshots
├── .env.example                      # Template for environment variables
├── docker-compose.yml                # Multi-container setup (PostgreSQL, MinIO, Apache Airflow)
├── requirements.txt                  # Python dependencies (boto3, pandas, pyarrow, sqlalchemy, dbt-postgres)
└── README.md