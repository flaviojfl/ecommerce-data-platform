"""Teste sem Python workers - usa só Spark SQL puro."""
from utils.spark_session import create_spark_session


def main() -> None:
    spark = create_spark_session("test-sql")

    print("\n=== Teste 1: Spark SQL puro ===")
    spark.sql("SELECT 1 as numero, 'hello' as texto").show()

    print("\n=== Teste 2: range ===")
    spark.range(5).show()

    spark.stop()


if __name__ == "__main__":
    main()