"""Helpers para leitura de tabelas MySQL via JDBC."""
import os

from pyspark.sql import DataFrame, SparkSession


def read_mysql_table(spark: SparkSession, table: str) -> DataFrame:
    """Lê uma tabela do MySQL via JDBC e retorna um DataFrame.

    Args:
        spark: SparkSession ativa.
        table: nome da tabela a ler.

    Returns:
        DataFrame com o conteúdo da tabela.
    """
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