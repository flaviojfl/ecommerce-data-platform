"""Hello World do PySpark — versão com schema explícito (compatível com Python 3.12 no Windows)."""
from pyspark.sql.types import DoubleType, StringType, StructField, StructType

from utils.spark_session import create_spark_session


def main() -> None:
    spark = create_spark_session("hello-spark")

    # Define schema explicitamente (boa prática em produção)
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

    print("\n=== DataFrame original ===")
    df.show()

    print("\n=== Schema explícito ===")
    df.printSchema()

    print("\n=== Total de compras por estado ===")
    df.groupBy("estado").sum("valor_compra").show()

    spark.stop()


if __name__ == "__main__":
    main()