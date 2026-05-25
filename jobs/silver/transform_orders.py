import os

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

BRONZE = "s3a://lakehouse/bronze"
SILVER = "s3a://lakehouse/silver"


def create_spark() -> SparkSession:
    minio_user = os.getenv("MINIO_ROOT_USER", "admin")
    minio_password = os.getenv("MINIO_ROOT_PASSWORD", "minioadmin123")
    return (
        SparkSession.builder
        .appName("silver-transform-orders")
        .master("spark://spark-master:7077")
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")
        .config("spark.hadoop.fs.s3a.access.key", minio_user)
        .config("spark.hadoop.fs.s3a.secret.key", minio_password)
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.sql.shuffle.partitions", "8")
        .getOrCreate()
    )


def main() -> None:
    spark = create_spark()
    spark.sparkContext.setLogLevel("WARN")

    orders = spark.read.parquet(f"{BRONZE}/orders")

    orders_clean = (
        orders
        .dropDuplicates(["order_id"])
        .filter(F.col("order_id").isNotNull())
        .withColumn("order_purchase_timestamp", F.to_timestamp("order_purchase_timestamp"))
        .withColumn("order_approved_at", F.to_timestamp("order_approved_at"))
        .withColumn("order_delivered_customer_date", F.to_timestamp("order_delivered_customer_date"))
        .withColumn("order_estimated_delivery_date", F.to_timestamp("order_estimated_delivery_date"))
        .withColumn("order_status", F.lower(F.trim(F.col("order_status"))))
        .drop("_ingestion_timestamp", "_source_system")
    )

    customers = spark.read.parquet(f"{BRONZE}/customers")
    customers_clean = (
        customers
        .dropDuplicates(["customer_id"])
        .withColumn("customer_state", F.upper(F.trim(F.col("customer_state"))))
        .drop("_ingestion_timestamp", "_source_system")
    )

    orders_clean.write.mode("overwrite").parquet(f"{SILVER}/orders")
    customers_clean.write.mode("overwrite").parquet(f"{SILVER}/customers")

    print(f"\nSilver orders: {orders_clean.count():,} linhas")
    print(f"Silver customers: {customers_clean.count():,} linhas")
    print("\n=== Silver concluída! ===")
    spark.stop()


if __name__ == "__main__":
    main()