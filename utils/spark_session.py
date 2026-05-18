"""Spark session builder with common configurations."""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).parent.parent / ".env")


java_home = os.getenv("JAVA_HOME")
if java_home:
    os.environ["JAVA_HOME"] = java_home

hadoop_home = os.getenv("HADOOP_HOME")
if hadoop_home:
    os.environ["HADOOP_HOME"] = hadoop_home
    
    os.environ["PATH"] = f"{hadoop_home}\\bin;{os.environ.get('PATH', '')}"

# Aponta workers do PySpark pro mesmo Python da venv
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession  # noqa: E402


def create_spark_session(app_name: str = "ecommerce-platform") -> SparkSession:
    """Create a Spark session configured for local development.

    Args:
        app_name: Name shown in Spark UI.

    Returns:
        Configured SparkSession instance.
    """
    print(f"Using JAVA_HOME: {os.environ.get('JAVA_HOME')}")
    print(f"Using HADOOP_HOME: {os.environ.get('HADOOP_HOME')}")
    print(f"Using PYSPARK_PYTHON: {os.environ.get('PYSPARK_PYTHON')}")

    # JVM options necessárias pro Java 17
    jvm_options = (
        "--add-opens=java.base/java.lang=ALL-UNNAMED "
        "--add-opens=java.base/java.lang.invoke=ALL-UNNAMED "
        "--add-opens=java.base/java.lang.reflect=ALL-UNNAMED "
        "--add-opens=java.base/java.io=ALL-UNNAMED "
        "--add-opens=java.base/java.net=ALL-UNNAMED "
        "--add-opens=java.base/java.nio=ALL-UNNAMED "
        "--add-opens=java.base/java.util=ALL-UNNAMED "
        "--add-opens=java.base/java.util.concurrent=ALL-UNNAMED "
        "--add-opens=java.base/sun.nio.ch=ALL-UNNAMED "
        "--add-opens=java.base/sun.nio.cs=ALL-UNNAMED "
        "--add-opens=java.base/sun.security.action=ALL-UNNAMED"
    )

    spark = (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .config("spark.sql.shuffle.partitions", "4")
        .config("spark.driver.memory", "2g")
        .config("spark.driver.extraJavaOptions", jvm_options)
        .config("spark.executor.extraJavaOptions", jvm_options)
        .config("spark.sql.execution.arrow.pyspark.enabled", "true")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    return spark