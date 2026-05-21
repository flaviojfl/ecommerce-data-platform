"""Spark session configurada para conectar no cluster e no MinIO (S3)."""
import os

from pyspark.sql import SparkSession


HADOOP_AWS_VERSION = "3.3.4"
AWS_SDK_VERSION = "1.12.262"


def create_spark_s3_session(app_name: str = "ecommerce-s3") -> SparkSession:
    """Cria SparkSession conectada ao cluster com suporte a S3/MinIO.

    Lê as credenciais do MinIO das variáveis de ambiente.
    """
    minio_user = os.getenv("MINIO_ROOT_USER", "admin")
    minio_password = os.getenv("MINIO_ROOT_PASSWORD", "minioadmin123")

    spark = (
        SparkSession.builder
        .appName(app_name)
        .master("spark://spark-master:7077")
        
        .config(
            "spark.jars.packages",
            f"org.apache.hadoop:hadoop-aws:{HADOOP_AWS_VERSION},"
            f"com.amazonaws:aws-java-sdk-bundle:{AWS_SDK_VERSION}",
        )
    
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")
        .config("spark.hadoop.fs.s3a.access.key", minio_user)
        .config("spark.hadoop.fs.s3a.secret.key", minio_password)
       
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
       
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
        .config(
            "spark.hadoop.fs.s3a.impl",
            "org.apache.hadoop.fs.s3a.S3AFileSystem",
        )
        .config("spark.sql.shuffle.partitions", "4")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    return spark