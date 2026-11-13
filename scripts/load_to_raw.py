import io
import datetime
import pandas as pd
import psycopg2
from minio import Minio
from config.settings import settings
from config.logger import get_logger

logger = get_logger("step2_load")

def init_minio_client() -> Minio:
    """Khởi tạo MinIO Client"""
    return Minio(
        settings.MINIO_ENDPOINT,
        settings.MINIO_ROOT_USER,
        settings.MINIO_ROOT_PASSWORD,
        secure=False
    )

def init_postgres_connection():
    """Khởi tạo kết nối PostgreSQL"""
    return psycopg2.connect(
        dbname=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT
    )
    

def load_single_table_to_postgres(table_name: str, minio_client: Minio) -> bool:
    """Tải file từ MinIO, gắn _ingested_at trên RAM và nạp vào PostgreSQL bằng COPY"""
    csv_filename = f"{table_name}.csv"
    response = None
    conn = None
    cursor = None
    
    try:
        logger.info(f"🔄 Processing table: {table_name} from MinIO to PostgreSQL...")
        
        # 1. Lấy stream dữ liệu từ MinIO Raw Bucket
        response = minio_client.get_object(settings.BUCKET_RAW, csv_filename)
        
        # 2. Đọc qua Pandas (ép kiểu string toàn bộ để bảo toàn dữ liệu thô)
        df = pd.read_csv(response, dtype=str)
        
        # 3. Gắn thêm cột _ingested_at (thời điểm nạp vào kho Warehouse)
        df['_ingested_at'] = datetime.datetime.now()
        
        # 4. Chuyển DataFrame thành dạng buffer CSV lưu tạm trên RAM
        buffer = io.StringIO()
        df.to_csv(buffer, index=False, header=False)
        buffer.seek(0)

        # 5. Kết nối PostgreSQL và dùng lệnh COPY nguyên bản tốc độ cao
        conn = init_postgres_connection()
        cursor = conn.cursor()

        # Lấy danh sách tên cột (bao gồm các cột gốc và cột _ingested_at mới thêm)
        columns = ','.join(list(df.columns))
        cursor.execute(f"TRUNCATE TABLE raw.{table_name} ;")
        sql_query = f"COPY raw.{table_name} ({columns}) FROM STDIN WITH CSV"
        
        cursor.copy_expert(sql_query, buffer)
        conn.commit()

        logger.info(f"✅ Ingested [raw.{table_name}] ({len(df):,} rows).")
        return True

    except Exception as e:
        logger.error(f"❌ Error ingesting table {table_name}: {e}")
        if conn:
            conn.rollback()
        return False
        
    finally:
        # Dọn dẹp tài nguyên kết nối an toàn
        if response:
            response.close()
            response.release_conn()
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn:
            conn.close()

def run_load_pipeline():
    """Chạy toàn bộ tiến trình nạp dữ liệu cho tất cả các bảng Olist"""
    logger.info("🚀Start processing get data from minio to postgres (Raw Layer)...")
    try:
        minio_client = init_minio_client()
    except Exception as e:
        logger.error(f"❌ Error initializing connections: {e}")
        return

    success_count = 0
    fail_count = 0
    
    try:
        # Chuyển kết quả list_objects thành list tĩnh ngay từ đầu để tránh giữ stream mở
        objects = list(minio_client.list_objects(settings.BUCKET_RAW, recursive=True))
    except Exception as e:
        logger.error(f"❌ Error listing objects from MinIO bucket: {e}")
        return

    # Lặp qua toàn bộ danh sách bảng Olist được định nghĩa trong settings
    for obj in objects:
        file_name = obj.object_name # ex: olist.customers_dataset.csv
        table_name = file_name.replace('.csv', '')
        
        
        success = load_single_table_to_postgres(table_name, minio_client)
        if success:
            success_count += 1
        else:
            fail_count += 1

    logger.info(f"🎉  Load success: {success_count}, Failed: {fail_count}")

if __name__ == "__main__":
    run_load_pipeline()