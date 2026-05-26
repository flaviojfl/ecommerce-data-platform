import os

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import (
    DoubleType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)

GOLD = "s3a://lakehouse/gold/streaming"
CHECKPOINT = "s3a://lakehouse/_checkpoints/clickstream"


def create_spark() -> SparkSession:
    minio_user = os.getenv("MINIO_ROOT_USER", "admin")
    minio_password = os.getenv("MINIO_ROOT_PASSWORD", "minioadmin123")
    return (
        SparkSession.builder
        .appName("streaming-clickstream")
        .master("spark://spark-master:7077")
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")
        .config("spark.hadoop.fs.s3a.access.key", minio_user)
        .config("spark.hadoop.fs.s3a.secret.key", minio_password)
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.sql.shuffle.partitions", "4")
        .getOrCreate()
    )


def main() -> None:
    spark = create_spark()
    spark.sparkContext.setLogLevel("WARN")

    schema = StructType([
        StructField("event_id", StringType()),
        StructField("user_id", StringType()),
        StructField("action", StringType()),
        StructField("category", StringType()),
        StructField("state", StringType()),
        StructField("value", DoubleType()),
        StructField("event_timestamp", TimestampType()),
    ])

    raw = (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "kafka:9092")
        .option("subscribe", "clickstream")
        .option("startingOffsets", "latest")
        .load()
    )

    eventos = (
        raw
        .select(F.from_json(F.col("value").cast("string"), schema).alias("data"))
        .select("data.*")
        .withWatermark("event_timestamp", "2 minutes")
    )

    agregado = (
        eventos
        .groupBy(
            F.window("event_timestamp", "1 minute"),
            "state",
            "action",
        )
        .agg(F.count("*").alias("total_eventos"))
    )

    query = (
        agregado.writeStream
        .format("parquet")
        .option("path", GOLD)
        .option("checkpointLocation", CHECKPOINT)
        .outputMode("append")
        .trigger(processingTime="30 seconds")
        .start()
    )

    print("Streaming iniciado. Processando a cada 30s. Ctrl+C para parar.")
    query.awaitTermination()


if __name__ == "__main__":
    main()