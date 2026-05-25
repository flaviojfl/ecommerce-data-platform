import os

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

SILVER = "s3a://lakehouse/silver"
GOLD = "s3a://lakehouse/gold"


def create_spark() -> SparkSession:
    minio_user = os.getenv("MINIO_ROOT_USER", "admin")
    minio_password = os.getenv("MINIO_ROOT_PASSWORD", "minioadmin123")
    return (
        SparkSession.builder
        .appName("gold-build-metrics")
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

    orders = spark.read.parquet(f"{SILVER}/orders")
    customers = spark.read.parquet(f"{SILVER}/customers")

    orders_by_status = (
        orders
        .groupBy("order_status")
        .agg(F.count("order_id").alias("total_orders"))
        .orderBy(F.desc("total_orders"))
    )
    orders_by_status.write.mode("overwrite").parquet(f"{GOLD}/orders_by_status")

    orders_with_state = orders.join(customers, on="customer_id", how="inner")
    orders_by_state = (
        orders_with_state
        .groupBy("customer_state")
        .agg(F.count("order_id").alias("total_orders"))
        .orderBy(F.desc("total_orders"))
    )
    orders_by_state.write.mode("overwrite").parquet(f"{GOLD}/orders_by_state")

    print("\n=== Pedidos por status ===")
    orders_by_status.show()

    print("\n=== Top estados por volume de pedidos ===")
    orders_by_state.show(10)

    print("\n=== Gold concluída! ===")
    spark.stop()


if __name__ == "__main__":
    main()