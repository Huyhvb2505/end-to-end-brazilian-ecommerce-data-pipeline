import os 
from minio import Minio
from minio.error import S3Error


def upload_data_to_minio():
    minio_client = Minio(
        "minio:9000",
        access_key=os.getenv("MINIO_ROOT_USER"),
        secret_key=os.getenv("MINIO_ROOT_PASSWORD"),
        secure=False
    )

    bucket_name = "raw-data"
    object_name = "./data/raw/"
    try:
        # check bucket có tồn tại ko nếu ko thì tạo 
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)


        # lay cac file .csv va upload len minio
        print(f"Bắt đầu upload dữ liệu từ {object_name} lên MinIO...")
        for file_name in os.listdir(object_name):
            if file_name.endswith(".csv"):
                file_path = os.path.join(object_name, file_name)

        #start upload data into minio
        minio_client.fput_object(
            bucket_name, 
            object_name, 
            file_path
        )
        
        print("\n--- Hoàn thành Ingestion! Dữ liệu đã sẵn sàng trên Data Lake. ---")
    except S3Error as e:
         print(f"Lỗi khi tương tác với MinIO: {e}")

if __name__ == "__main__":
    upload_data_to_minio()