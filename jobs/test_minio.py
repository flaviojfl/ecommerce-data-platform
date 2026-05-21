"""Testa escrita e leitura no MinIO via Spark (s3a)."""
from pyspark.sql.types import DoubleType, StringType, StructField, StructType

from utils.spark_s3 import create_spark_s3_session


def main() -> None:
    spark = create_spark_s3_session("test-minio")

    schema = StructType([
        StructField("nome", StringType(), nullable=False),
        StructField("estado", StringType(), nullable=False),
        StructField("valor_compra", DoubleType(), nullable=False),
    ])

    data = [
        ("Alice", "SP", 1500.0),
        ("Bob", "RJ", 2300.0),
        ("Carol", "SP", 1800.0),
    ]

    df = spark.createDataFrame(data, schema=schema)

   
    output_path = "s3a://lakehouse/test/compras"
    print(f"\n=== Escrevendo em {output_path} ===")
    df.write.mode("overwrite").parquet(output_path)
    print("Escrita concluída!")

   
    print(f"\n=== Lendo de {output_path} ===")
    df_lido = spark.read.parquet(output_path)
    df_lido.show()

    print(f"\n=== Total de linhas lidas: {df_lido.count()} ===")

    spark.stop()


if __name__ == "__main__":
    main()