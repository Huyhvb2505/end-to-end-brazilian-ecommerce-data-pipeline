import os
from pathlib import Path
import pandas as pd
from  config.settings import settings
from minio import Minio
from sqlalchemy import create_engine # interact with postgreSQL

# create bronze func -> transform csv file to parquet + push minio + load to postgres
def run_bronze_pipeline():
    print("🚀 Starting Bronze Layer pipeline...")
    
    # 1.initial Minio client
    #  settings.MINIO_ENDPOINT, settings.MINIO_ROOT_USER, settings.MINIO_ROOT_PASSWORD
    minio_client = Minio(
       settings.MINIO_ENDPOINT,
       settings.MINIO_ROOT_USER,
       settings.MINIO_ROOT_PASSWORD,
       secure=False
    )

    # check and create bucket raw-data on MINIO if not exists
    # TODO: write check command bucket_exists and make_bucket with settings.BUCKET_RAW

    if not minio_client.bucket_exists(settings.BUCKET_RAW):
        minio_client.make_bucket(settings.BUCKET_RAW)
        print(f"✅ Created MinIO Bucket: {settings.BUCKET_RAW}")
        
    # ==================postgres======================
    # 2. initial postgres engine  
    # TODO: create engine with settings.POSTGRES_CONN_STR
    engine = create_engine(settings.POSTGRES_CONN_STR)
    
    # Đảm bảo schema 'raw' đã tồn tại trong Postgres
    with engine.begin() as conn:
        conn.execute("CREATE SCHEMA IF NOT EXISTS raw;")
    print("✅ Created schema 'raw' in PostgreSQL.")

    # 3. loop through each Olist table
    for table_name in settings.OLIST_TABLES:
        file_name = f"{table_name}.csv"
        csv_path = settings.RAW_DATA_DIR / file_name
        
        if not csv_path.exists():
            print(f"⚠️ Warning: File doesn’t exist: {file_name}.")
            continue

        parquet_filename = f"{table_name}.parquet"
        parquet_path = settings.TEMP_DIR / parquet_filename

        print(f"\n🔄 Processing table: {table_name}")

        # --- BƯỚC 1: Đọc CSV -> Chuyển sang Parquet ---
        df = pd.read_csv(csv_path)
        df.to_parquet(parquet_path)

        # --- BƯỚC 2: Upload into MinIO ---
        minio_client.fput_object(settings.BUCKET_RAW, parquet_filename, str(parquet_path))
        print(f"   -> Uploaded to MinIO: {settings.BUCKET_RAW}/{parquet_filename}")
        
        
        # --- BƯỚC 3: Load vào PostgreSQL (schema raw) ---
        df.to_sql(name=table_name, 
                  con=engine, schema="raw", 
                  if_exists="replace", 
                  index=False,
                  chunksize=50000)  # split into chunks of 50,000 rows
        print(f"   -> Loaded to Postgres table: [raw].[{table_name}]")

    print("\n🎉 Successfully completed Bronze Layer pipeline!")
    
if __name__ == "__main__":
    run_bronze_pipeline()