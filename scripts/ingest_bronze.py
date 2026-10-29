import os
from pathlib import Path
import pandas as pd
from  config.settings import settings
from minio import Minio
from sqlalchemy import create_engine

# --- 1. CONFIGURATION ---
# Có thể load từ file config/settings.py hoặc biến môi trường (.env)
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minio_admin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minio_password")
BUCKET_NAME = "bronze"

POSTGRES_CONN_STR = os.getenv(
    "POSTGRES_CONN_STR", 
    "postgresql://postgres:postgres@localhost:5432/ecommerce_dw" # Thay đổi thông tin user/pass/db theo docker-compose của bạn
)

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
TEMP_PARQUET_DIR = BASE_DIR / "data" / "temp_parquet"
TEMP_PARQUET_DIR.mkdir(parents=True, exist_ok=True)

# Danh sách các file CSV Olist
csv_files = [
    "olist_customers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "product_category_name_translation.csv"
]

def run_bronze_pipeline():
    # Khởi tạo MinIO client
    minio_client = Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False
    )

    if not minio_client.bucket_exists(BUCKET_NAME):
        minio_client.make_bucket(BUCKET_NAME)
        print(f"✅ Created MinIO Bucket: {BUCKET_NAME}")

    # Khởi tạo PostgreSQL engine
    engine = create_engine(POSTGRES_CONN_STR)

    for file_name in csv_files:
        csv_path = RAW_DATA_DIR / file_name
        if not csv_path.exists():
            print(f"⚠️ Warning: Không tìm thấy file {file_name} trong {RAW_DATA_DIR}, bỏ qua.")
            continue

        table_name = file_name.replace(".csv", "")
        parquet_filename = f"{table_name}.parquet"
        parquet_path = TEMP_PARQUET_DIR / parquet_filename

        print(f"\n🔄 Đang xử lý bảng: {table_name}")

        # Bước 1: Đọc CSV -> Chuyển sang Parquet
        df = pd.read_csv(csv_path)
        df.to_parquet(parquet_path, engine="pyarrow", index=False)
        print(f"   -> Đã chuyển đổi sang Parquet thành công.")

        # Bước 2: Upload file Parquet lên MinIO (Landing Zone)
        object_name = f"olist/{parquet_filename}"
        minio_client.fput_object(BUCKET_NAME, object_name, str(parquet_path))
        print(f"   -> Đã upload lên MinIO: {bucket_name}/{object_name}")

        # Bước 3: Load dữ liệu từ DataFrame vào PostgreSQL (Schema: raw)
        # Sử dụng if_exists='replace' để ghi đè sạch sẽ ở tầng raw, chunksize giúp tối ưu memory
        df.to_sql(
            name=table_name,
            con=engine,
            schema="raw",
            if_exists="replace",
            index=False,
            chunksize=50000
        )
        print(f"   -> Đã load vào PostgreSQL thành công tại schema [raw].[{table_name}]")

    print("\n🎉 Hoàn tất toàn bộ Bronze Layer pipeline!")

if __name__ == "__main__":
    # Đảm bảo schema raw đã được tạo trong postgres trước khi insert
    with create_engine(POSTGRES_CONN_STR).begin() as conn:
        conn.execute("CREATE SCHEMA IF NOT EXISTS raw;")
    
    run_bronze_pipeline()