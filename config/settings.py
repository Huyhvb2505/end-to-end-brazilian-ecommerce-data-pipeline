from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType

def get_spark_session(app_name="Brazilian-Ecommerce"):
    return SparkSession.builder \
        .appName(app_name) \
        .master("spark://spark-master:7077") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .config("spark.jars.packages", "org.postgresql:postgresql:42.6.0,org.apache.hadoop:hadoop-aws:3.3.4") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
        .config("spark.hadoop.fs.s3a.access.key", "minio_admin") \
        .config("spark.hadoop.fs.s3a.secret.key", "minio_secure_pwd") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
        .config("spark.executor.memory", "1g") \
        .config("spark.driver.memory", "1g") \
        .getOrCreate()

BRONZE_PATHS = {
    "customers": "s3a://raw-data/olist_customers_dataset.csv",
    # TODO: bạn điền tiếp 8 bảng còn lại
}

# TODO: bạn copy lại toàn bộ dict `schemas` đã viết ở validate_BronzeData.ipynb vào đây
# nhớ thêm multiLine cho reviews — nhưng multiLine là .option(), không nằm trong schema,
# nên bạn cần nghĩ cách lưu thông tin "bảng này cần .option() đặc biệt" — gợi ý bên dưới

TABLE_OPTIONS = {
    "reviews": {"multiLine": "true"},
    # các bảng khác không cần, để dict rỗng hoặc bỏ qua
}