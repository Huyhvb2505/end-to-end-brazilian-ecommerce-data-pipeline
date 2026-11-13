from  config.settings import settings
from minio import Minio
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



# create bronze func -> transform csv file to parquet + push minio + load to postgres
def process_single_table(table_name: str, minio_client: Minio) -> bool:
    """Xử lý toàn bộ luồng ETL cho 1 bảng cụ thể: CSV  -> MinIO ."""
    csv_file_name = f"{table_name}.csv"
    csv_path = settings.RAW_DATA_DIR / csv_file_name
    
    # check if file exists
    if not csv_path.exists():
        logger.warning(f"⚠️ Warning: File doesn’t exist: {csv_file_name}.")
        return False


    try:
        # Upload lên MinIO
        minio_client.fput_object(
            settings.BUCKET_RAW, 
            csv_file_name, 
            str(csv_path))
        
        logger.info(f"    -> Uploaded to MinIO: {settings.BUCKET_RAW}/{csv_file_name}")        
        return True

    except Exception as e:
        logger.error(f"❌ Error processing table {table_name}: {e}")
        return False

def run_ingest_pipeline(): 
    logger.info("🚀 Starting Bronze Layer pipeline...")
    
    try:
        minio_client = init_minio_client()
    except Exception as e:
        logger.critical(f"❌ Error initializing resources: {e}")
        return

    success_count = 0
    fail_count = 0

    # Loop through each Olist table
    for table_name in settings.OLIST_TABLES:
        success = process_single_table(table_name, minio_client)
        if success:
            success_count += 1
        else:
            fail_count += 1

    logger.info(f"🎉 Completed Bronze Layer pipeline! Success: {success_count}, Failed: {fail_count}")

if __name__ == "__main__":
    run_ingest_pipeline()