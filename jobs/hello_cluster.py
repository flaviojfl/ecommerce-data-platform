"""Hello World rodando no cluster Spark (dentro do Docker)."""
from pyspark.sql import SparkSession
from pyspark.sql.types import DoubleType, StringType, StructField, StructType


def main() -> None:
    # Conecta no master do cluster (nome do serviço na network Docker)
    spark = (
        SparkSession.builder
        .appName("hello-cluster")
        .master("spark://spark-master:7077")
        .config("spark.sql.shuffle.partitions", "4")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    schema = StructType([
        StructField("nome", StringType(), nullable=False),
        StructField("estado", StringType(), nullable=False),
        StructField("valor_compra", DoubleType(), nullable=False),
    ])

    data = [
        ("Alice", "SP", 1500.0),
        ("Bob", "RJ", 2300.0),
        ("Carol", "SP", 1800.0),
        ("David", "MG", 950.0),
        ("Eve", "RJ", 3100.0),
    ]

    df = spark.createDataFrame(data, schema=schema)

    print("\n=== Total de compras por estado (no cluster!) ===")
    df.groupBy("estado").sum("valor_compra").show()

    spark.stop()


if __name__ == "__main__":
    main()