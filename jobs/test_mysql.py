"""Testa leitura de tabelas do MySQL via JDBC."""
from pyspark.sql import SparkSession

from utils.mysql_jdbc import read_mysql_table


def main() -> None:
    spark = (
        SparkSession.builder
        .appName("test-mysql")
        .master("spark://spark-master:7077")
        .config("spark.sql.shuffle.partitions", "4")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    # Lê as três tabelas
    for table in ["customers", "products", "orders"]:
        print(f"\n=== Tabela: {table} ===")
        df = read_mysql_table(spark, table)
        df.show()
        print(f"Total de linhas: {df.count()}")

    spark.stop()


if __name__ == "__main__":
    main()
    