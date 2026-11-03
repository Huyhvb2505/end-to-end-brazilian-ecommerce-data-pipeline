import os
import datetime
from pathlib import Path
import pandas as pd
from  config.settings import settings
from minio import Minio
from sqlalchemy import create_engine # interact with postgreSQL
from config.logger import get_logger

logger = get_logger("ingest_bronze")


# Initialize MinIO client function
def init_minio_client() -> Minio:
    # 1.initial Minio client
    #  settings.MINIO_ENDPOINT, settings.MINIO_ROOT_USER, settings.MINIO_ROOT_PASSWORD
    minio_client = Minio(
       settings.MINIO_ENDPOINT,
       settings.MINIO_ROOT_USER,
       settings.MINIO_ROOT_PASSWORD,
       secure=False
    ) 
    if not minio_client.bucket_exists(settings.BUCKET_RAW):
        minio_client.make_bucket(settings.BUCKET_RAW)
        logger.info(f"✅ Created MinIO Bucket: {settings.BUCKET_RAW}")
        
    return minio_client

# Initialize PostgreSQL engine function
def init_postgres_engine():
    #initial sqlalchemy engine 
    engine = create_engine(settings.POSTGRES_CONN_STR)
    
    with engine.begin() as conn:
        conn.execute("CREATE SCHEMA IF NOT EXISTS raw;")
    logger.info("✅ Created schema 'raw' in PostgreSQL.")
    return engine

# create bronze func -> transform csv file to parquet + push minio + load to postgres
def process_single_table(table_name: str, minio_client: Minio, engine) -> bool:
    """Xử lý toàn bộ luồng ETL cho 1 bảng cụ thể: CSV -> Parquet -> MinIO -> Postgres."""
    file_name = f"{table_name}.csv"
    csv_path = settings.RAW_DATA_DIR / file_name
    
    if not csv_path.exists():
        logger.warning(f"⚠️ Warning: File doesn’t exist: {file_name}.")
        return False

    parquet_filename = f"{table_name}.parquet"
    parquet_path = settings.TEMP_DIR / parquet_filename

    logger.info(f"🔄 Processing table: {table_name}")

    try:
        # Step 1: Đọc CSV và ép kiểu string toàn bộ để tránh mất dữ liệu
        df = pd.read_csv(csv_path, dtype=str)
        Path(parquet_path).parent.mkdir(parents=True, exist_ok=True)

        # Step 2: Thêm metadata thời gian nạp
        df['_ingested_at'] = datetime.datetime.now()

        # Step 3: Lưu ra file Parquet và Upload lên MinIO
        df.to_parquet(parquet_path, index=False)
        minio_client.fput_object(settings.BUCKET_RAW, parquet_filename, str(parquet_path))
        logger.info(f"    -> Uploaded to MinIO: {settings.BUCKET_RAW}/{parquet_filename}")

        # Step 4: Load vào PostgreSQL (schema raw) theo từng chunk
        df.to_sql(
            name=table_name, 
            con=engine, 
            schema="raw", 
            if_exists="replace",  
            index=False,
            chunksize=50000
        )
        logger.info(f"    -> Loaded to Postgres table: [raw].[{table_name}]")
        return True

    except Exception as e:
        logger.error(f"❌ Error processing table {table_name}: {e}")
        return False
    
def run_bronze_pipeline(): 
    logger.info("🚀 Starting Bronze Layer pipeline...")

    # Initialize resources
    try:
        minio_client = init_minio_client()
        engine = init_postgres_engine()
    
    except Exception as e:
        logger.critical(f"❌ Error initializing resources: {e}")
        return
    success_count = 0
    fail_count = 0

        # 3. loop through each Olist table
    for table_name in settings.OLIST_TABLES:
        success = process_single_table(table_name, minio_client, engine)
        if success:
            success_count += 1
        else:
            fail_count += 1

    logger.info(f"🎉 Completed Bronze Layer pipeline! Success: {success_count}, Failed: {fail_count}")

if __name__ == "__main__":
    run_bronze_pipeline()