
import os

from pyspark.sql import SparkSession
from pyspark.sql import functions as F


TABLES = ["customers", "orders", "products", "sellers"]

BRONZE_PATH = "s3a://lakehouse/bronze"


def create_spark() -> SparkSession:
    """SparkSession configurada para cluster + MinIO."""
    minio_user = os.getenv("MINIO_ROOT_USER", "admin")
    minio_password = os.getenv("MINIO_ROOT_PASSWORD", "minioadmin123")

    return (
        SparkSession.builder
        .appName("bronze-ingest-mysql")
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


def read_mysql_table(spark: SparkSession, table: str):
    """Lê uma tabela do MySQL via JDBC."""
    mysql_user = os.getenv("MYSQL_USER", "spark_user")
    mysql_password = os.getenv("MYSQL_PASSWORD", "sparkpass123")
    mysql_database = os.getenv("MYSQL_DATABASE", "ecommerce")
    jdbc_url = f"jdbc:mysql://mysql:3306/{mysql_database}"

    return (
        spark.read
        .format("jdbc")
        .option("url", jdbc_url)
        .option("driver", "com.mysql.cj.jdbc.Driver")
        .option("dbtable", table)
        .option("user", mysql_user)
        .option("password", mysql_password)
        .load()
    )


def main() -> None:
    spark = create_spark()
    spark.sparkContext.setLogLevel("WARN")

    for table in TABLES:
        print(f"\n=== Ingerindo '{table}' ===")

       
        df = read_mysql_table(spark, table)
        row_count = df.count()
        print(f"  {row_count:,} linhas lidas do MySQL")

        
        df_bronze = (
            df
            .withColumn("_ingestion_timestamp", F.current_timestamp())
            .withColumn("_source_system", F.lit("mysql"))
        )

        
        output_path = f"{BRONZE_PATH}/{table}"
        df_bronze.write.mode("overwrite").parquet(output_path)
        print(f"  Escrito em {output_path}")

    print("\n=== Ingestão Bronze (MySQL) concluída! ===")
    spark.stop()


if __name__ == "__main__":
    main()