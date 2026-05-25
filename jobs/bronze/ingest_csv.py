import os

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

CSV_TO_TABLE = {
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_geolocation_dataset.csv": "geolocation",
    "product_category_name_translation.csv": "category_translation",
}

CSV_DIR = "/app/data/raw/olist"
BRONZE_PATH = "s3a://lakehouse/bronze"


def create_spark() -> SparkSession:
    minio_user = os.getenv("MINIO_ROOT_USER", "admin")
    minio_password = os.getenv("MINIO_ROOT_PASSWORD", "minioadmin123")
    return (
        SparkSession.builder
        .appName("bronze-ingest-csv")
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

    for csv_name, table in CSV_TO_TABLE.items():
        print(f"\n=== Ingerindo '{table}' ===")
        csv_path = f"{CSV_DIR}/{csv_name}"

        df = (
            spark.read
            .option("header", "true")
            .option("inferSchema", "true")
            .option("multiLine", "true")
            .option("escape", '"')
            .csv(csv_path)
        )
        row_count = df.count()
        print(f"  {row_count:,} linhas lidas de {csv_name}")

        df_bronze = (
            df
            .withColumn("_ingestion_timestamp", F.current_timestamp())
            .withColumn("_source_system", F.lit("csv"))
        )

        output_path = f"{BRONZE_PATH}/{table}"
        df_bronze.write.mode("overwrite").parquet(output_path)
        print(f"  Escrito em {output_path}")

    print("\n=== Ingestão Bronze (CSV) concluída! ===")
    spark.stop()


if __name__ == "__main__":
    main()