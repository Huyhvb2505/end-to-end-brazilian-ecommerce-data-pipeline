import os
from pathlib import Path
from dotenv import load_dotenv

# 1. Tự động load file .env ở thư mục gốc của project
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings:
    # --- Directory Structure ---
    BASE_DIR = BASE_DIR
    RAW_DATA_DIR = BASE_DIR / "data" / "raw"
    TEMP_DIR = BASE_DIR / "data" / "temp_parquet"

    # --- JUPYTER CONFIG ---
    JUPYTER_PORT = int(os.getenv("JUPYTER_PORT", 8888))
    JUPYTER_TOKEN = os.getenv("JUPYTER_TOKEN", "")

    # --- POSTGRES CONFIG ---
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "brazilian_ecommerce_dw")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "de_user")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
    AIRFLOW_DB_NAME = os.getenv("AIRFLOW_DB_NAME", "airflow_metadata")

    # Tạo sẵn chuỗi kết nối chuẩn cho PostgreSQL Data Warehouse
    POSTGRES_CONN_STR = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
        f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    # --- MINIO CONFIG ---
    MINIO_HOST = os.getenv("MINIO_HOST", "localhost")
    MINIO_API_PORT = os.getenv("MINIO_API_PORT", "9000")
    MINIO_CONSOLE_PORT = os.getenv("MINIO_CONSOLE_PORT", "9001")
    MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER", "minio_admin")
    MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD", "")
    
    # Endpoint để kết nối từ Python client
    MINIO_ENDPOINT = f"{MINIO_HOST}:{MINIO_API_PORT}"

    # --- BUCKETS CONFIG ---
    BUCKET_RAW = os.getenv("BUCKET_RAW", "raw-data")
    BUCKET_PROCESSED = os.getenv("BUCKET_PROCESSED", "processed-data")
    BUCKET_MODELS = os.getenv("BUCKET_MODELS", "ml-models")

    # --- AIRFLOW CONFIG ---
    AIRFLOW_IMAGE_NAME = os.getenv("AIRFLOW_IMAGE_NAME", "apache/airflow:2.8.1-python3.10")
    AIRFLOW_UID = int(os.getenv("AIRFLOW_UID", 50000))
    AIRFLOW_USER = os.getenv("_AIRFLOW_WWW_USER_USERNAME", "admin")
    AIRFLOW_PASSWORD = os.getenv("_AIRFLOW_WWW_USER_PASSWORD", "admin")

    # --- OLIST TABLES (Danh sách các bảng dataset gốc) ---
    OLIST_TABLES = [
        "olist_customers_dataset",
        "olist_geolocation_dataset",
        "olist_order_items_dataset",
        "olist_order_payments_dataset",
        "olist_order_reviews_dataset",
        "olist_orders_dataset",
        "olist_products_dataset",
        "olist_sellers_dataset",
        "product_category_name_translation"
    ]

# Initialize settings
settings = Settings()