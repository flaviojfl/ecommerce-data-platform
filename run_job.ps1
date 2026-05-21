# run_job.ps1 - Helper para rodar jobs PySpark no cluster Docker
# Uso: .\run_job.ps1 jobs/test_mysql.py

param(
    [Parameter(Mandatory=$true)]
    [string]$JobPath
)

$packages = "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262,com.mysql:mysql-connector-j:8.4.0"

docker compose exec -e PYTHONPATH=/app spark-client `
    /opt/spark/bin/spark-submit `
    --master spark://spark-master:7077 `
    --packages $packages `
    --conf spark.jars.ivy=/tmp/.ivy2 `
    "/app/$JobPath"